import uuid

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal

from App.api.api_constants import HTTP_CREATE_SUCCESS, HTTP_OK, REGISTER, LOGIN
from App.api.utils import get_user, current_user
from App.extensions import cache
from App.models.admin.admin_user_model import AdminModel


parse = reqparse.RequestParser()
parse.add_argument("username", type=str, required=True, help="请输入用户名")
parse.add_argument("password", type=str, required=True, help="请输入密码")
parse.add_argument("action", type=str, required=True, help="请确认请求参数")

admin_fields = {
    "name": fields.String,
}
single_admin_fields = {
    "status": fields.String,
    "msg": fields.String,
    "data":fields.Nested(admin_fields)
}

class AdminResources(Resource):

    def post(self):
        """
        用户注册和登录api
        :return:
        """

        args = parse.parse_args()
        username = args.get("username")
        password = args.get("password")
        action = args.get("action")

        if action == REGISTER:
            admin = AdminModel()
            admin.name = username
            admin.password = password

            if not admin.save():
                abort(400, msg="注册失败")

            data = {
                "status":HTTP_CREATE_SUCCESS,
                "msg": "ok",
                "data": admin,
                }
            return marshal(data, single_admin_fields)
        elif action == LOGIN:
            admin = get_user(username, AdminModel)
            if not admin:
                abort(400, msg="用户不存在")
            if not admin.check_password(password):
                abort(401, msg="用户名或密码错误")
            token = create_access_token(identity=admin.name)
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
        customer = current_user(get_jwt_identity(), AdminModel)
        data = {
            "status": 200,
            "msg": "ok",
            "data":customer
        }
        return marshal(data, single_admin_fields)

