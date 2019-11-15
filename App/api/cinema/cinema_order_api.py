import datetime

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, fields, marshal, abort

from App.api.cinema.cinema_api import cinema_fields
from App.api.common.movies_api import movie_fields
from App.api.utils import permission_required, valid_seats, current_user, parse_seats
from App.models.cinema.cinema_hall_model import HallModel
from App.models.cinema.cinema_order_model import CinemaOrderModel
from App.models.cinema.hall_movie_model import HallMovieModel
from App.models.model_constants import COMMON_CINEMA_ADMIN, COMMON_CUSTOMER

parse = reqparse.RequestParser()
parse.add_argument("hall_id", type=int)
parse.add_argument("movie_id", type=int)
parse.add_argument("hall_movie_id", type=int)


"""
    cinema_id = models.Column(models.Integer, models.ForeignKey(CinemaModel.id))
    hall_id = models.Column(models.Integer, models.ForeignKey(HallModel.id))
    movie_id = models.Column(models.Integer, models.ForeignKey(MovieModel.id))
    hall_movie_id = models.Column(models.Integer, models.ForeignKey(HallMovieModel.id))
    order_time = models.Column(models.DateTime)
    order_status = models.Column(models.Integer, default=ORDER_WAITING_PAYMENT)
    total_price = models.Column(models.Float, default=0)
    seats = models.Column(models.String(64))
    
"""

cinema_order_fields = {
    "cinema_id":fields.Integer,
    "hall_id":fields.Integer,
    "movie_id":fields.Integer,
    "hall_movie_id":fields.Integer,
    "order_time":fields.DateTime,
    "order_status":fields.Integer,
    "total_price":fields.Float,
    "seats":fields.String,
    "customer_id":fields.Integer,
}

class CinemaOrdersResource(Resource):
    @jwt_required
    @permission_required(COMMON_CINEMA_ADMIN)
    def get(self):
        args = parse.parse_args()
        hall_id = args.get("hall_id")
        movie_id = args.get("movie_id")
        hall_movie_id = args.get("hall_id")

        filtered_orders = CinemaOrderModel.query.all()
        if hall_id:
            filtered_orders = filtered_orders.filter(CinemaOrderModel.hall_id == hall_id)
        if movie_id:
            filtered_orders = filtered_orders.filter(CinemaOrderModel.movie_id == hall_id)
        if hall_movie_id:
            filtered_orders = filtered_orders.filter(CinemaOrderModel.hall_movie_id == hall_movie_id)
        orders = filtered_orders.all()

        data = {
            "status":200,
            "msg":"ok",
            "data":[marshal(order, cinema_order_fields) for order in orders]
        }
        return data


order_create_parse = reqparse.RequestParser()
order_create_parse.add_argument("seats", type=str, required=True, help="请选择座位"

                                )
class CinemaOrderResource(Resource):
    @jwt_required
    @permission_required(COMMON_CUSTOMER)
    def get(self, id):
        order = CinemaOrderModel.query.get(id)
        if not order or order.customer_id != current_user().id:
            abort(400, msg="请求被拒绝")
        data = {
            "status":200,
            "msg":"ok",
            "data":marshal(order, cinema_order_fields)
        }
        return data

    @jwt_required
    @permission_required(COMMON_CUSTOMER)
    def post(self, id):
        hall_movie = HallMovieModel.query.get(id)
        if not hall_movie:
            abort(400, msg="参数错误")
        if datetime.datetime.now() - hall_movie.date_time < datetime.timedelta(minutes=10):
            abort(400, msg="已停止购票")
        hall_id = hall_movie.hall_id
        movie_id = hall_movie.movie_id
        hall = HallModel.query.get(hall_id)
        cinema_id = hall.cinema_id
        seats = order_create_parse.parse_args().get("seats")
        if not valid_seats(seats, hall_id):
            abort(400, msg="座位不可选")
        order = CinemaOrderModel()
        order.hall_id = hall_id
        order.movie_id = movie_id
        order.hall_movie_id = id
        order.cinema_id = cinema_id
        order.customer_id = current_user().id
        order.seats = seats
        order.price = len(parse_seats(seats)) * hall_movie.price
        if not order.save():
            abort(400, msg="订单创建失败")

        data = {
            "status": 201,
            "msg": "created",
            "data": marshal(order, cinema_order_fields)
        }
        return data



