from flask_restful import Api

from App.api.customer.customer_orders import OrdersResource
from App.api.customer.customers_api import CustomersResources
from App.api.customer.filter import MoviesFilterResource, CinemasFilterResource

client_api = Api(prefix="/user")

client_api.add_resource(CustomersResources, "/")
client_api.add_resource(OrdersResource, "/orders/")
client_api.add_resource(MoviesFilterResource, "/movies/")
client_api.add_resource(CinemasFilterResource, "/cinemas/")
