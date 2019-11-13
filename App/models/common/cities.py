from App.extensions import models
from App.models import BaseModel


class CityLetterModel(BaseModel):
    letter = models.Column(models.String(1), unique=True)


class CitiesModel(BaseModel):
    letter_id = models.Column(models.Integer, models.ForeignKey(CityLetterModel.id))
    city_id = models.Column(models.Integer, default=0)
    city_parent_id = models.Column(models.Integer, default=0)
    city_code = models.Column(models.Integer, default=0)
    city_name = models.Column(models.String(64))
    city_pinyin = models.Column(models.String(64))