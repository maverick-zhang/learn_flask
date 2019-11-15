import uuid

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_current_user, get_jwt_claims
from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal

from App.api.api_constants import HTTP_CREATE_SUCCESS, REGISTER, LOGIN, HTTP_OK
from App.api.utils import get_user, current_user, permission_required
from App.extensions import cache
from App.models.cinema.cinema_user_model import CinemaUserModel
from App.models.model_constants import COMMON_CINEMA_ADMIN

parse = reqparse.RequestParser()
parse.add_argument("username", type=str, required=True, help="请输入用户名")
parse.add_argument("password", type=str, required=True, help="请输入密码")
parse.add_argument("phone", type=str, required=True, help="请输入手机号")
parse.add_argument("cinema_id", type=int, required=True, help="请提供影院")
user_operation_parse = parse.copy()
parse.add_argument("action", type=str, required=True, help="请确认请求参数")

cinema_user_fields = {
    "name": fields.String,
    "phone": fields.String,
    "cinema_id": fields.Integer,
}

class CinemaUsersResources(Resource):

    def post(self):
        """
        用户注册和登录api
        :return:
        """

        args = parse.parse_args()
        username = args.get("username")
        password = args.get("password")
        phone = args.get("phone")
        action = args.get("action")
        cinema_id = args.get("cinema_id")

        if action == REGISTER:
            cinema_user = CinemaUserModel()
            cinema_user.name = username
            cinema_user.password = password
            cinema_user.phone = phone
            cinema_user.cinema_id = cinema_id

            if not cinema_user.save():
                abort(400, msg="注册失败")

            data = {
                "status":HTTP_CREATE_SUCCESS,
                "msg": "ok",
                "data": marshal(cinema_user, cinema_user_fields),
                }
            return data
        elif action == LOGIN:
            cinema_user = get_user(username, CinemaUserModel) or get_user(phone, CinemaUserModel)
            if not cinema_user:
                abort(400, msg="用户不存在")
            if not cinema_user.check_password(password):
                abort(401, msg="用户名或密码错误")
            token = create_access_token(identity=cinema_user.name, user_claims={"role":"cinema_user"})
            data = {
                "status": HTTP_OK,
                "msg": "ok",
                "token": token
            }
            return data

        else:
            abort(400, msg="请提供正确的参数")


class CinemaUserResource(Resource):
    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def get(self, id):
        cinema_user = current_user()
        if not isinstance(cinema_user, CinemaUserModel):
            cinema_user = CinemaUserModel.query.get(id)
            if not cinema_user:
                abort(400, msg="参数不正确")
        data = {
            "status": 200,
            "msg": "ok",
            "data":marshal(cinema_user, cinema_user_fields)
        }
        return data


    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def patch(self, id):
        cinema_user = current_user()
        if not isinstance(cinema_user, CinemaUserModel):
            cinema_user = CinemaUserModel.query.get(id)
            if not cinema_user:
                abort(400, msg="参数不正确")
        args = user_operation_parse.parse_args()
        username = args.get("username")
        password = args.get("password")
        phone = args.get("phone")
        cinema_id = args.get("cinema_id")
        cinema_user.name = username
        cinema_user.password = password
        cinema_user.phone = phone
        cinema_user.cinema_id = cinema_id
        cinema_user.save()
        data = {
            "status": 200,
            "msg": "ok",
            "data":marshal(cinema_user, cinema_user_fields)
        }
        return data



