from os import access
from venv import create
from flask_restful import Resource, reqparse
from sqlalchemy import Identity
from models.user import UserModel
from blacklist import BLACKLIST
from hmac import compare_digest
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
    )

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )



class UserRegister(Resource):
    def post(self):
        data = _user_parser.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

class UserLogin(Resource):

    def post(cls):
        data = _user_parser.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        # This is what authenticate() function used to do
        if user and compare_digest(user.password, data['password']):
            # identity = is what identity() function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message', 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jti is "JWT ID", a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully Logout'}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, freah=False)
        return {'access_token': new_token}, 200
