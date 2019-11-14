from flask_jwt_extended import jwt_required
from flask_restful import Resource

from App.api.utils import permission_required, current_user
from App.models.model_constants import COMMON_CUSTOMER


class OrdersResource(Resource):
    @jwt_required
    @permission_required(COMMON_CUSTOMER)
    def get(self):
        customer = current_user()
        data = {
            "status":200,
            "msg": "ok",
            "data":"to do",
            "username":customer.name,
        }
        return data


