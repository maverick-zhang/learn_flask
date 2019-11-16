import datetime
import time

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, marshal, fields, abort
from sqlalchemy import or_

from App.api.cinema.cinema_hall_api import hall_fields
from App.api.common.movies_api import movie_fields
from App.api.utils import permission_required, current_user, available_seats
from App.models.cinema.cinema_hall_model import HallModel
from App.models.cinema.cinema_movie_model import CinemaMovieModel
from App.models.cinema.cinema_order_model import CinemaOrderModel, ORDER_SUCCESS, ORDER_WAITING_PAYMENT
from App.models.cinema.hall_movie_model import HallMovieModel
from App.models.common.movies import MovieModel
from App.models.model_constants import COMMON_CINEMA_ADMIN

parse = reqparse.RequestParser()
parse.add_argument("hall_id", type=int, help="请提供放映厅编号", required=True)
parse.add_argument("date_time", help="请选择排挡时间", required=True)

hall_movie_fields = {
    "hall_id": fields.Integer,
    "movie_id": fields.Integer,
    "date_time": fields.DateTime,
}


class HallMoviesResource(Resource):
    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def get(self):
        args = parse.parse_args()
        date_time = datetime.datetime.strptime(args.get("date_time"), "%Y-%m-%d %H:%M:%S")
        hall_movies = HallMovieModel.query.filter(HallMovieModel.hall_id == args.get("hall_id")).\
                                           filter(HallMovieModel.date_time == date_time).all()
        data = {
            "status":200,
            "msg": "ok",
            "data": [marshal(hall_movie, hall_movie_fields) for hall_movie in hall_movies]
        }
        return data

    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def post(self):
        hall_movie_post_parse = parse.copy()
        hall_movie_post_parse.add_argument("movie_id", type=int, required=True, help="请选择电影")
        hall_movie = HallMovieModel()
        args = hall_movie_post_parse.parse_args()
        movie_id = args.get("movie_id")
        hall_id = args.get("hall_id")
        date_time = datetime.datetime.strptime(args.get("date_time"), "%Y-%m-%d %H:%M:%S")
        hall_movie.date_time = date_time
        hall_movie.hall_id = hall_id
        hall_movie.movie_id = movie_id

        cinema_id = current_user().cinema_id
        halls = HallModel().query.filter(HallModel.cinema_id == cinema_id).all()
        halls_id = [hall.id for hall in halls]
        if hall_id not in halls_id:
            abort(400, msg="非法参数")

        movies = CinemaMovieModel.query.filter(CinemaMovieModel.cinema_id == cinema_id).all()
        movies_id = [movie.id for movie in movies]
        if movie_id not in movies_id:
            abort(400, msg="非法参数")

        if date_time - datetime.datetime.now() < datetime.timedelta(days=1):
            abort(400, msg="请提前一天排片")

        if not hall_movie.save():
            abort(400, msg="创建失败")
        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(hall_movie, hall_movie_fields)
        }
        return data


class HallMovieResource(Resource):
    @jwt_required
    @permission_required
    def get(self, id):
        hall_movie = HallMovieModel.query.get(id)
        if not hall_movie:
            abort(400, msg="参数错误")
        hall_id = hall_movie.hall_id
        hall = HallModel.query.get(hall_id)
        safe_seats = available_seats(id, hall_id)
        hall.seats = safe_seats
        movie = MovieModel.query.get(hall_movie.movie_id)
        movie_hall = {
            "movie": movie,
            "hall": hall,
        }
        movie_hall_fields = {
            "movie":fields.Nested(movie_fields),
            "hall": fields.Nested(hall_fields)
        }

        data = {
            "status":200,
            "msg": "ok",
            "data": marshal(movie_hall, movie_hall_fields)
        }
        return data

