from App.extensions import models
from App.models import BaseModel
from App.models.cinema.cinema_model import CinemaModel


class HallModel(BaseModel):
    cinema_id = models.Column(models.Integer, models.ForeignKey(CinemaModel.id))
    hall_num = models.Column(models.Integer, unique=True)
    seats = models.Column(models.String(2048))