from App.extensions import models
from App.models import BaseModel
from App.models.cinema.cinema_model import CinemaModel
from App.models.common.movies import MovieModel


class CinemaMovieModel(BaseModel):
    cinema_id = models.Column(models.Integer, models.ForeignKey(CinemaModel.id), nullable=False)
    movie_id = models.Column(models.Integer, models.ForeignKey(MovieModel.id), nullable=False)

