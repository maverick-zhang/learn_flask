from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, marshal, abort

from App.api.cinema.cinema_api import cinema_fields
from App.api.utils import permission_required, current_user
from App.models.cinema.cinema_model import CinemaModel
from App.models.model_constants import SUPER_CINEMA_ADMIN

parse = reqparse.RequestParser()
parse.add_argument("name", required=True, help="请输入影院名称")
parse.add_argument("city", required=True, help="请输入影院城市")
parse.add_argument("district", required=True, help="请输入影院地区")
parse.add_argument("address", required=True, help="请输入影院详细地址")
parse.add_argument("phone", required=True, help="请输入影院联系电话")
parse.add_argument("is_verified", type=bool, required=True, help="请确认影院是否通过后验证")


class CinemasResource(Resource):
    @jwt_required
    @permission_required(SUPER_CINEMA_ADMIN)
    def get(self):
        cinemas = CinemaModel.query.all()
        data = {
            "status":200,
            "msg": "ok",
            "data": [marshal(cinema, cinema_fields) for cinema in cinemas]
        }
        return data


class CinemaAdminResource(Resource):
    @jwt_required
    @permission_required(SUPER_CINEMA_ADMIN)
    def get(self, id):
        cinema = CinemaModel.query.get(id)
        if not cinema:
            abort(400, msg="参数不正确")
        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(cinema, cinema_fields)
        }
        return data


    @jwt_required
    @permission_required(SUPER_CINEMA_ADMIN)
    def put(self, id):
        cinema = CinemaModel.query.get(id)
        if not cinema:
            abort(400, msg="参数不正确")
        args = parse.parse_args()
        cinema.city = args.get("city")
        cinema.name = args.get("name")
        cinema.district = args.get("district")
        cinema.phone = args.get("phone")
        cinema.address = args.get("address")
        cinema.save()

        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(cinema, cinema_fields)
        }
        return data


    @jwt_required
    @permission_required(SUPER_CINEMA_ADMIN)
    def post(self):
        args = parse.parse_args()
        cinema = CinemaModel()
        cinema.city = args.get("city")
        cinema.name = args.get("name")
        cinema.district = args.get("district")
        cinema.phone = args.get("phone")
        cinema.address = args.get("address")
        cinema.is_verified = args.get("is_verified")
        cinema.save()

        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(cinema, cinema_fields)
        }

        return data