from flask_restful import Api

from App.api.cinema.cinema_api import CinemaResource
from App.api.cinema.cinema_hall_api import CinemaHallResource
from App.api.cinema.cinema_movie_api import CinemaMovieResource, CinemaMoviesResource
from App.api.cinema.cinema_order_api import CinemaOrdersResource, CinemaOrderResource
from App.api.cinema.cinema_user_api import CinemaUsersResources, CinemaUserResource
from App.api.cinema.hall_movie_api import HallMoviesResource, HallMovieResource

cinema_client_api = Api(prefix="/cinema")
cinema_client_api.add_resource(CinemaUsersResources, "/users/")
cinema_client_api.add_resource(CinemaUserResource, "/user/")
cinema_client_api.add_resource(CinemaResource, "/<int:id>/")
cinema_client_api.add_resource(CinemaMoviesResource, "/movies/")
cinema_client_api.add_resource(CinemaMovieResource, "/movie/<int:id>/")
cinema_client_api.add_resource(CinemaHallResource, "/hall/")
cinema_client_api.add_resource(HallMoviesResource, "/hallmovies/")
cinema_client_api.add_resource(HallMovieResource, "/hallmovie/<int:id>/")
cinema_client_api.add_resource(CinemaOrdersResource, "/orders/")
cinema_client_api.add_resource(CinemaOrderResource, "/order/<int:id>/")