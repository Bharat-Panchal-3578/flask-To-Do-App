from flask import Blueprint
from flask_restful import Api

auth_bp = Blueprint("auth",__name__, template_folder='templates')
api = Api(auth_bp)

from . import routes
from .api_routes import RegisterResource, LoginResource, RefreshTokenResource, LogoutResource

api.add_resource(RegisterResource,"/api/register")
api.add_resource(LoginResource,"/api/login")
api.add_resource(RefreshTokenResource,"/api/refresh")
api.add_resource(LogoutResource,"/api/logout")