from App.extensions import models
from App.models import BaseModel
from App.models.cinema.cinema_hall_model import HallModel
from App.models.common.movies import MovieModel


class HallMovieModel(BaseModel):
    movie_id = models.Column(models.Integer, models.ForeignKey(MovieModel.id))
    hall_id = models.Column(models.Integer, models.ForeignKey(HallModel.id))
    date_time = models.Column(models.DateTime)
    price = models.Column(models.Float)

