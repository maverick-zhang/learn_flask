import uuid

from flask_jwt_extended import get_jwt_identity, get_jwt_claims
from flask_restful import abort

from App.models.admin.admin_user_model import AdminModel
from App.models.cinema_admin.cinema_user_model import CinemaUserModel
from App.models.customer.customers import CustomerModel
from App.models.model_constants import BLACK_LIST_USER


def get_user(ident, model):
    user = model.query.get(ident)
    if user:
        return user
    elif model.query.filter(model.name == ident).first():
        user = model.query.filter(model.name == ident).first()
        return user
    else:
        return False


def current_user():
    ident = get_jwt_identity()
    role = get_jwt_claims()["role"]
    if role == "customer":
        model = CustomerModel
    elif role == "admin":
        model = AdminModel
    elif role == "cinema_user":
        model = CinemaUserModel
    else:
        abort(400, msg="非法用户")
    user = model.query.filter(model.name == ident).first()
    return user


def permission_required(permission):
    def permission_required_wrapper(func):
        def wrapper(*args, **kwargs):
            user = current_user()
            if user.permission == BLACK_LIST_USER:
                abort(403, msg="you are in blacklist")
            if not user.permission >= permission:
                abort(403, msg="permission denied")
            # print(user.name, args, kwargs, func)
            return func(*args, **kwargs)
        return wrapper
    return permission_required_wrapper



def file_name_transfer(filename):
    return uuid.uuid4().hex + filename