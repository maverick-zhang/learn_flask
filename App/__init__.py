from flask import Flask

from App.api import init_api
from App.extensions import  init_ext
from App.settings import envs


def create_app(env):
    # 默认的模板路径为当前路径
    app = Flask(__name__)
    app.config.from_object(envs.get(env))
    init_ext(app)
    init_api(app)
    return app