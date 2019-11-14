from flask_restful import Api

from App.api.cinema_admin.cinema_api import CinemasResource, CinemaResource
from App.api.cinema_admin.cinema_user_api import CinemaUsersResources

cinema_client_api = Api(prefix="/cinema")
cinema_client_api.add_resource(CinemaUsersResources, "/users/")
cinema_client_api.add_resource(CinemasResource, "/cinemas/")
cinema_client_api.add_resource(CinemaResource, "/cinema/<int:id>/")
