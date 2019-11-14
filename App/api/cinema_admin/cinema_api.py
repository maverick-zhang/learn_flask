from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, fields, marshal

from App.api.utils import permission_required, current_user
from App.models.cinema_admin.cinema_model import CinemaModel
from App.models.model_constants import COMMON_CINEMA_ADMIN, SUPER_CINEMA_ADMIN
"""
    cinema_admin_id = models.Column(models.Integer, models.ForeignKey(CinemaUserModel.id))
    name = models.Column(models.String(64))
    city = models.Column(models.String(16))
    district = models.Column(models.String(16))
    address = models.Column(models.String(128))
    phone = models.Column(models.String(16))
    score = models.Column(models.Float, default=10)
    hallNum = models.Column(models.Integer, default=1)
    serviceCharge = models.Column(models.Float, default=10)
    aStrict = models.Column(models.Float, default=10)
    flag = models.Column(models.Boolean, default=False)
    is_delete = models.Column(models.Boolean, default=False)
"""
parse = reqparse.RequestParser()
parse.add_argument("name", required=True, help="请输入影院名称")
parse.add_argument("city", required=True, help="请输入影院城市")
parse.add_argument("district", required=True, help="请输入影院地区")
parse.add_argument("address", required=True, help="请输入影院详细地址")
parse.add_argument("phone", required=True, help="请输入影院联系电话")

cinema_fields = {
    "cinema_admin_id": fields.Integer,
    "name": fields.String,
    "city": fields.String,
    "district": fields.String,
    "address": fields.String,
    "phone": fields.String,
    "score": fields.Float,
    "hallNum": fields.Integer,
    "serviceCharge": fields.Float,
    "aStrict": fields.Float,
    "flag": fields.Boolean,
    "is_delete": fields.Boolean,
}

class CinemasResource(Resource):
    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def get(self):
        data = {
            "status":200,
            "msg": "ok",

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
        cinema.cinema_admin_id = current_user().id
        cinema.save()

        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(cinema, cinema_fields)
        }

        return data


class CinemaResource(Resource):
    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def get(self, id):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass