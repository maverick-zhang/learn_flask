from App.api.admin import admin_api
from App.api.common import common_api
from App.api.cinema import cinema_client_api
from App.api.customer import client_api


def init_api(app):
    client_api.init_app(app)
    cinema_client_api.init_app(app)
    admin_api.init_app(app)
    common_api.init_app(app)
