import uuid

from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal

from App.api.api_constants import HTTP_CREATE_SUCCESS, CUSTOMER_ACTION_REGISTER, CUSTOMER_ACTION_LOGIN, HTTP_OK
from App.api.movie_user.model_utils import get_customer
from App.extensions import cache
from App.models.movie_user.customers import CustomerModel


parse = reqparse.RequestParser()
parse.add_argument("username", type=str, required=True, help="请输入用户名")
parse.add_argument("password", type=str, required=True, help="请输入密码")
parse.add_argument("phone", type=str, required=True, help="请输入手机号")
parse.add_argument("action", type=str, required=True, help="请确认请求参数")

customer_fields = {
    "name": fields.String,
    "phone": fields.String,
}
single_customer_fields = {
    "status": fields.String,
    "msg": fields.String,
    "data":fields.Nested(customer_fields)
}

class CustomersResources(Resource):

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

        if action == CUSTOMER_ACTION_REGISTER:
            customer = CustomerModel()
            customer.name = username
            customer.password = password
            customer.phone = phone

            if not customer.save():
                abort(400, msg="注册失败")

            data = {
                "status":HTTP_CREATE_SUCCESS,
                "msg": "ok",
                "data": customer,
                }
            return marshal(data, single_customer_fields)
        elif action == CUSTOMER_ACTION_LOGIN:
            customer = get_customer(username) or get_customer(phone)
            if not customer:
                abort(400, msg="用户不存在")
            if not customer.check_password(password):
                abort(401, msg="用户名或密码错误")
            token = uuid.uuid4().hex
            cache.set(token, customer.name, timeout=60*60*24*7)
            data = {
                "status": HTTP_OK,
                "msg": "ok",
                "token": token
            }
            return data

        else:
            abort(400, msg="请提供正确的参数")

