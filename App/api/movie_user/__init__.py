from flask_restful import Api

from App.api.movie_user.customers_api import CustomersResources

client_api = Api(prefix="/user")

client_api.add_resource(CustomersResources, "/")