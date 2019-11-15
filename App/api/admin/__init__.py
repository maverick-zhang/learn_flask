from flask_restful import Api

from App.api.admin.admin_api import AdminResources
from App.api.admin.cinema_admin_api import CinemasResource, CinemaAdminResource

admin_api = Api(prefix="/admin")

admin_api.add_resource(AdminResources, "/")

admin_api.add_resource(CinemasResource, "/cinemas/")
admin_api.add_resource(CinemaAdminResource, "/cinema/")

