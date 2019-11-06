from App.views.blue1 import blue
from App.views.second import second


def init_view(app):
    app.register_blueprint(blue)
    app.register_blueprint(second)