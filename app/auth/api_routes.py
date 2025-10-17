from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models import User
from app.extensions import db
from app.utils import success_response, error_response
from app.models import BlackListedToken

class RegisterResource(Resource):
    def post(self):
        pass

class LoginResource(Resource):
    def post(self):
        pass

class RefreshTokenResource(Resource):
    def post(self):
        pass

class LogoutResource(Resource):
    def post(self):
        pass