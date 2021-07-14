from datetime import datetime, timedelta
from werkzeug.security import safe_str_cmp
from app.main.model.user import User
from flask_jwt import JWT
from flask import current_app

jwt = JWT()


@jwt.authentication_handler
def authenticate(email, password):
    user = User.find_by_email(email)
    if user and user.check_password(password):
        return user


@jwt.identity_handler
def identity(payload):
    user_id = payload['user_id']
    return User.find_by_id(user_id)


@jwt.jwt_payload_handler
def make_payload(identity):
    iat = datetime.utcnow()
    exp = iat + \
        current_app.config.get('JWT_EXPIRATION_DELTA', timedelta(seconds=5))
    nbf = iat + \
        current_app.config.get('JWT_NOT_BEFORE_DELTA', timedelta(seconds=0))
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'user_id': identity.id}
