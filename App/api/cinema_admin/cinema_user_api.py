import uuid

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_current_user, get_jwt_claims
from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal

from App.api.api_constants import HTTP_CREATE_SUCCESS, REGISTER, LOGIN, HTTP_OK
from App.api.utils import get_user, current_user
from App.extensions import cache
from App.models.cinema_admin.cinema_user_model import CinemaUserModel


parse = reqparse.RequestParser()
parse.add_argument("username", type=str, required=True, help="请输入用户名")
parse.add_argument("password", type=str, required=True, help="请输入密码")
parse.add_argument("phone", type=str, required=True, help="请输入手机号")
parse.add_argument("action", type=str, required=True, help="请确认请求参数")

cinema_user_fields = {
    "name": fields.String,
    "phone": fields.String,
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

        if action == REGISTER:
            cinema_user = CinemaUserModel()
            cinema_user.name = username
            cinema_user.password = password
            cinema_user.phone = phone

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


    @jwt_required
    def get(self):
        cinema_user = current_user()
        print(get_jwt_claims()["role"])
        data = {
            "status": 200,
            "msg": "ok",
            "data":marshal(cinema_user, cinema_user_fields)
        }
        return data


