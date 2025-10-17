from flask import Blueprint
from flask_restful import Api
from . import routes
from .api_routes import RegisterResource, LoginResource, RefreshTokenResource, LogoutResource

auth_bp = Blueprint("auth",__name__)
api = Api(auth_bp)
api.add_resource(RegisterResource,"/register")
api.add_resource(LoginResource,"/login")
api.add_resource(RefreshTokenResource,"/refresh")
api.add_resource(LogoutResource,"/logout")