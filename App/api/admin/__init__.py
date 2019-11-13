from flask_restful import Api

from App.api.admin.admin_api import AdminResources

admin_api = Api(prefix="/admin")

admin_api.add_resource(AdminResources, "/")