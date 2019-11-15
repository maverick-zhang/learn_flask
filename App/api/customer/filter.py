import datetime

from flask_restful import Resource, reqparse, marshal, fields

from App.api.cinema.hall_movie_api import hall_movie_fields
from App.models.cinema.cinema_hall_model import HallModel
from App.models.cinema.cinema_model import CinemaModel
from App.models.cinema.hall_movie_model import HallMovieModel

movie_filter_parse = reqparse.RequestParser()
movie_filter_parse.add_argument("movie_id", type=str, required=True, help="电影名不能为空")
movie_filter_parse.add_argument("city", type=str)
movie_filter_parse.add_argument("district", type=str)

cinema_filter_parse = reqparse.RequestParser()
cinema_filter_parse.add_argument("city", type=str)
cinema_filter_parse.add_argument("district", type=str)

cinema_filter_fields = {
    "name":fields.String,
    "city":fields.String,
    "district":fields.String,
    "score":fields.Float,
    "id":fields.Integer,
}

class MoviesFilterResource(Resource):
    def get(self):
        args = movie_filter_parse.parse_args()
        movie_id = args.get("name")
        city = args.get("city")
        district = args.get("district")
        filtered_movies = HallMovieModel.query.filter(HallMovieModel.date_time > datetime.datetime.now()).\
                                              filter(HallMovieModel.id == movie_id)
        cinemas = []
        if city:
            cinemas = CinemaModel.query.filter(CinemaModel.city == city)
        if district:
            cinemas = CinemaModel.query.filter(CinemaModel.district == district).all()
        if cinemas:
            halls_id = []
            for cinema in cinemas:
                halls_id += HallModel.query.filter(HallModel.cinema_id == cinema.id).all()
            filtered_movies= filtered_movies.filter(HallMovieModel.hall_id in halls_id)
        hall_movies = filtered_movies.all()
        data = {
            "status": 200,
            "msg":"ok",
            "data":[marshal(hall_movie, hall_movie_fields) for hall_movie in hall_movies]
        }
        return data


class CinemasFilterResource(Resource):
    def get(self):
        args = movie_filter_parse.parse_args()
        city = args.get("city")
        district = args.get("district")

        if city:
            cinemas = CinemaModel.query.filter(CinemaModel.city == city)
            if district:
                cinemas = CinemaModel.query.filter(CinemaModel.district == district).all()
        else:
            cinemas = CinemaModel.query.all()


        data = {
            "status": 200,
            "msg": "ok",
            "data": [marshal(cinema, cinema_filter_fields) for cinema in cinemas]
        }
        return data

