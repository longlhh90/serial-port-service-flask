from flask import Flask

from .config import config_by_name
from .services.auth import jwt
from app.init.db import db, flask_bcrypt
from app.init.api import api
from .services.user import *


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    api.init_app(app)
    jwt.init_app(app)

    @app.before_first_request
    def _create_tables():
        db.create_all()

    return app
