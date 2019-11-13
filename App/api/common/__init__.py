from flask_restful import Api

from App.api.common.cities_api import CitiesResource

cities_api = Api(prefix="/common")

cities_api.add_resource(CitiesResource, "/cities/")