import datetime

from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal, reqparse, abort
from werkzeug.datastructures import FileStorage

from App.api.utils import permission_required, file_name_transfer
from App.models.common.movies import MovieModel
from App.models.model_constants import SUPER_ADMIN
from App.settings import BASE_DIR

movie_fields = {
    "showName": fields.String,
    "showNameEn": fields.String,
    "director": fields.String,
    "leadingRole": fields.String,
    "movieType": fields.String,
    "country": fields.String,
    "language": fields.String,
    "duration": fields.Integer,
    "screeningModel": fields.String,
    "openDay": fields.DateTime,
    "bgPicture": fields.String,
    "flag": fields.Boolean(default=False),
    "is_delete": fields.Boolean(default=False),
}

parse = reqparse.RequestParser()
parse.add_argument("showName", type=str, required=True, help="请输入电影名称")
parse.add_argument("showNameEn", type=str, required=True, help="请输入电影英文名称")
parse.add_argument("director", type=str, required=True, help="请输入导演名称")
parse.add_argument("leadingRole", type=str, required=True, help="请输入主演")
parse.add_argument("movieType", type=str, required=True, help="请输入电影类型")
parse.add_argument("country", type=str, required=True, help="请输入电影归属国")
parse.add_argument("language", type=str, required=True, help="请输入电影语言")
parse.add_argument("openDay", required=True, help="请输入电影公映日期")
parse.add_argument("bgPicture", type=FileStorage, required=True, help="请输入电影海报", location=["files"])

class MoviesResource(Resource):
    def get(self):
        movies = MovieModel.query.all()
        print(movies[0])

        data = {
            "status": 200,
            "msg": "ok",
            "data": [marshal(movie, movie_fields) for movie in movies]
        }

        return data


    @jwt_required
    @permission_required(SUPER_ADMIN)
    def post(self):
        args = parse.parse_args()
        showName = args.get("showName")
        showNameEn = args.get("showNameEn")
        director = args.get("director")
        leadingRole = args.get("leadingRole")
        movieType = args.get("movieType")
        country = args.get("country")
        language = args.get("language")
        duration = args.get("duration")
        screeningModel = args.get("screeningModel")
        openDay = args.get("openDay")
        bgPicture = args.get("bgPicture")



        # backgroundpicture = request.files.get("backgroundpicture")

        movie = MovieModel()
        movie.showName = showName
        movie.showNameEn = showNameEn
        movie.director = director
        movie.leadingRole = leadingRole
        movie.movieType = movieType
        movie.country = country
        movie.language = language
        movie.duration = duration
        movie.screeningModel = screeningModel
        movie.openDay = datetime.datetime.strptime(openDay, "%Y-%m-%d")
        f_name = file_name_transfer(bgPicture.filename)
        print(f_name)
        movie.bgPicture = "static/uploads/icons/"+f_name
        bgPicture.save(BASE_DIR + "/App/static/uploads/icons/"+f_name)
        movie.save()

        data = {
            "status":201,
            "msg": "created",
            "data":marshal(movie, movie_fields)
        }
        return data


class MovieResource(Resource):
    def get(self, id):
        movie = MovieModel.query.get(id)
        if not movie:
            abort(404, msg="内容不存在")
        data = {
            "status":200,
            "msg":"ok",
            "data":marshal(movie, movie_fields)
        }
        return data