from flask import Flask

from App.ext import init_ext
from App.settings import Config
from App.views import init_view


def create_app():
    app = Flask(__name__)


    app.config.from_object(Config)
    init_ext(app)

    init_view(app)


    return app