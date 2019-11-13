from flask_jwt_extended import get_jwt_identity, get_current_user
from flask_restful import abort

from App.extensions import jwt
from App.models.movie_user.model_constants import COMMON_CUSTOMER, BLACK_LIST_USER, SUPER_ADMIN


def get_user(custom_id, model):
    user = model.query.get(custom_id)
    if user:
        return user
    elif model.query.filter(model.name == custom_id).first():
        user = model.query.filter(model.name == custom_id).first()

        return user
    else:
        return False


def current_user(identity, model):
    user = model.query.filter(model.name == identity).first()
    return user


def permission_required(permission, model):
    def permission_required_wrapper(func):
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user = current_user(identity, model)
            if user.permission == BLACK_LIST_USER:
                abort(403, msg="you are in blacklist")
            if not user.permission >= permission:
                abort(403, msg="permission denied")
            # print(user.name, args, kwargs, func)
            return func(*args, **kwargs)
        return wrapper
    return permission_required_wrapper
