from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity
from flask_restful import Resource

from App.api.utils import permission_required, current_user
from App.models.movie_user.customers import CustomerModel
from App.models.movie_user.model_constants import SUPER_ADMIN, COMMON_CUSTOMER


class OrdersResource(Resource):
    @jwt_required
    @permission_required(COMMON_CUSTOMER, CustomerModel)
    def get(self):
        customer = current_user(get_jwt_identity(), CustomerModel)
        data = {
            "status":200,
            "msg": "ok",
            "data":"to do",
            "username":customer.name,
        }
        return data


