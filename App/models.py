from App.ext import models


class User(models.Model):
    id = models.Column(models.Integer, primary_key=True)
    name = models.Column(models.String(20))
