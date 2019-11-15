from flask_jwt_extended import jwt_required
from flask_restful import Resource, marshal, fields, abort, reqparse

from App.api.utils import permission_required
from App.models.cinema.cinema_user_model import CinemaUserModel
from App.models.model_constants import SUPER_ADMIN

cinema_user_admin_fields = {
    "name": fields.String,
    "phone": fields.String,
    "is_delete":fields.Boolean,
    "is_verified":fields.Boolean,
    "is_super":fields.Boolean,
    "permission":fields.Integer,
    "cinema_id": fields.Integer,
}
parse = reqparse.RequestParser()
parse.add_argument("username", type=str, required=True, help="请输入用户名")
parse.add_argument("password", type=str, required=True, help="请输入密码")
parse.add_argument("phone", type=str, required=True, help="请输入手机号")
parse.add_argument("is_delete", type=bool, required=True, help="请确认是否删除")
parse.add_argument("is_super", type=bool, required=True, help="请确认是否为超级管理")
parse.add_argument("is_verified", type=bool, required=True, help="请确认是否通过验证")
parse.add_argument("permission", type=int, required=True, help="请提供权限值")
parse.add_argument("cinema_id", type=int, required=True, help="请提供影院")

class CinemaUsersAdminResource(Resource):
    @jwt_required
    @permission_required(SUPER_ADMIN)
    def get(self):
        users = CinemaUserModel.query.all()
        data = {
            "status": 200,
            "msg": "ok",
            "data":[marshal(user, cinema_user_admin_fields) for user in users]
        }
        return data


class CinemaUserAdminResource(Resource):

    @jwt_required
    @permission_required(SUPER_ADMIN)
    def get(self, id):
        cinema_user = CinemaUserModel.query.get(id)
        if not cinema_user:
            abort(400, msg="参数不正确")
        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(cinema_user, cinema_user_admin_fields)
        }
        return data

    @jwt_required
    @permission_required(SUPER_ADMIN)
    def put(self, id):
        cinema_user = CinemaUserModel.query.get(id)
        if not cinema_user:
            abort(400, msg="参数不正确")
        args = parse.parse_args()
        cinema_user.name = args.get("username")
        cinema_user.password = args.get("password")
        cinema_user.phone = args.get("phone")
        cinema_user.is_delete = args.get("is_delete")
        cinema_user.is_verified = args.get("is_verified")
        cinema_user.is_super = args.get("is_super")
        cinema_user.permission = args.get("permission")
        cinema_user.cinema_id = args.get("cinema_id")
        data = {
            "status": 200,
            "msg": "ok",
            "data": marshal(cinema_user, cinema_user_admin_fields)
        }

        return data
