from flask_restful import Api

from App.api.common.cities_api import CitiesResource
from App.api.common.movies_api import MoviesResource, MovieResource

common_api = Api(prefix="/common")

common_api.add_resource(CitiesResource, "/cities/")
common_api.add_resource(MoviesResource, "/movies/")
common_api.add_resource(MovieResource, "/movie/<int:id>/")