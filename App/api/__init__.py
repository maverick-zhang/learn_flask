from App.api.admin import admin_api
from App.api.common import cities_api
from App.api.movie_admin import movie_client_api
from App.api.movie_user import client_api


def init_api(app):
    client_api.init_app(app)
    movie_client_api.init_app(app)
    admin_api.init_app(app)
    cities_api.init_app(app)
