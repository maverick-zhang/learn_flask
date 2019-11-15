from flask_jwt_extended import jwt_required
from flask_restful import Resource, marshal, fields, abort

from App.api.utils import permission_required, current_user
from App.models.cinema.cinema_movie_model import CinemaMovieModel
from App.models.common.movies import MovieModel
from App.models.model_constants import COMMON_CINEMA_ADMIN

cinema_movie_fields = {
    "cinema_id": fields.Integer,
    "movie_id": fields.Integer,
}

class CinemaMoviesResource(Resource):
    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def get(self):
        user = current_user()
        cinema_movies = CinemaMovieModel.query.filter(CinemaMovieModel.cinema_id == user.cinema_id)
        data = {
            "status":200,
            "msg":"ok",
            "data":[marshal(cinema_movie, cinema_movie_fields) for cinema_movie in cinema_movies]
        }

        return data


class CinemaMovieResource(Resource):
    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def get(self, id):
        cinema_movie = CinemaMovieModel.query.get(id)
        if not cinema_movie:
            abort(400, msg="参数不正确")
        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(cinema_movie, cinema_movie_fields)
        }

        return data


    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def post(self, id):
        movie = MovieModel.query.get(id)
        if not movie:
            abort(400, msg="参数不正确")
        cinema_id = current_user().cinema_id
        cinema_movie = CinemaMovieModel.query.filter(CinemaMovieModel.movie_id == id).\
                                              filter(CinemaMovieModel.cinema_id == cinema_id)
        print(cinema_movie)
        if cinema_movie.first():
            abort(400, msg="已购买，无需重复购买")
        cinema_movie = CinemaMovieModel()
        cinema_movie.cinema_id = cinema_id
        cinema_movie.movie_id = id
        cinema_movie.save()
        return {
            "status":201,
            "msg":"购买成功"
        }