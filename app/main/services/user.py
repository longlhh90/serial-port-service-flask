from flask_restful import Resource, reqparse
from app.main.model.user import User
from flask_jwt import jwt_required
from app.init.api import api


@api.resource('/sign-up/')
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        user = User(data['email'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


@api.resource('/users/')
class Users(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument(
        'password',
        type=str,
        required=False,
        help="This field cannot be blank."
    )

    @jwt_required()
    def get(self):
        # TODO: improve with role
        # if current_identity.role == "admin":
        data = Users.parser.parse_args()
        user = User.find_by_email(data['email'])
        if not user:
            return {"response": "failed!!"}
        return user.json()

    @jwt_required()
    def put(self):
        # TODO: improve with role
        # if current_identity.role == "admin":
        data = Users.parser.parse_args()
        user = User.find_by_email(data['email'])
        if user:
            user.password = data["password"]
        else:
            user = User(**data)

        user.save_to_db()

        return user.json()
