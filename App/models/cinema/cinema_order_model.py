from App.extensions import models
from App.models import BaseModel
from App.models.cinema.cinema_hall_model import HallModel
from App.models.cinema.cinema_model import CinemaModel
from App.models.cinema.hall_movie_model import HallMovieModel
from App.models.common.movies import MovieModel
from App.models.customer.customers import CustomerModel

ORDER_WAITING_PAYMENT = 0
ORDER_SUCCESS = 1
ORDER_TIMEOUT = 2
ORDER_CANCELED = 3


class CinemaOrderModel(BaseModel):
    cinema_id = models.Column(models.Integer, models.ForeignKey(CinemaModel.id))
    hall_id = models.Column(models.Integer, models.ForeignKey(HallModel.id))
    movie_id = models.Column(models.Integer, models.ForeignKey(MovieModel.id))
    hall_movie_id = models.Column(models.Integer, models.ForeignKey(HallMovieModel.id))
    order_time = models.Column(models.DateTime)
    order_status = models.Column(models.Integer, default=ORDER_WAITING_PAYMENT)
    total_price = models.Column(models.Float, default=0)
    seats = models.Column(models.String(64))
    customer_id = models.Column(models.Integer, models.ForeignKey(CustomerModel.id))