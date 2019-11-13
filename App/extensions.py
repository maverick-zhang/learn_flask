from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import  SQLAlchemy

models = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache(config={
    "DEBUG": True,
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL": "redis://localhost/",
    "CACHE_DEFAULT_TIMEOUT": 3600
})

def init_ext(app):
    models.init_app(app)
    migrate.init_app(app, models)
    jwt.init_app(app)
    cache.init_app(app)
    DebugToolbarExtension(app)