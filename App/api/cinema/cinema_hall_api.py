from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, abort, marshal, fields

from App.api.utils import permission_required, current_user
from App.models.cinema.cinema_hall_model import HallModel
from App.models.model_constants import SUPER_CINEMA_ADMIN

parse = reqparse.RequestParser()
parse.add_argument("hall_num", type=int, required=True, help="请提供放映厅编号")
parse.add_argument("seats", type=str, required=True, help="请提供放映厅座位布局")

hall_fields = {
    "cinema_id": fields.Integer,
    "hall_num": fields.Integer,
    "seats": fields.String
}

class CinemaHallResource(Resource):
    @jwt_required
    @permission_required(SUPER_CINEMA_ADMIN)
    def post(self):
        args = parse.parse_args()
        user = current_user()
        hall = HallModel()
        hall.cinema_id = user.cinema_id
        hall.hall_num = args.get("hall_num")
        hall.seats = args.get("seats")
        if not hall.save():
            abort(400, msg="创建失败")
        return {
            "status":201,
            "msg": "created",
            "data":marshal(hall, hall_fields)
        }
