from flask import Blueprint

from App.ext import models
from App.models import User

blue = Blueprint('blue', __name__)


@blue.route('/createdb/')
def create_db():
    models.create_all()
    return "sucess"

@blue.route('/adduser/')
def adduser():
    user = User()
    user.name = 'tom'
    models.session.add(user)
    models.session.commit()
    return "success"