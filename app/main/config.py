import os
from datetime import datetime, timedelta
import dotenv

dotenv.load_dotenv()

BASEDIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", None)
    ENV = os.environ.get("FLASK_ENV", "development")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is required for Flask application")
    DEBUG = False
    # JWT AUTH CONFIG
    JWT_AUTH_USERNAME_KEY = "email"
    JWT_AUTH_PASSWORD_KEY = "password"
    JWT_EXPIRATION_DELTA = timedelta(seconds=1500)
    JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASEDIR, 'flask_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASEDIR, 'flask_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    ENV = os.environ.get("FLASK_ENV", "production")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY_PROD", None)
    # FIXME: move config to separated files and call config base on the file
    # if FLASK_ENV == "production" and not SECRET_KEY:
    #     raise ValueError(
    #         "No SECRET_KEY set for Flask application in Production")
    # FOR DB
    # ...


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
