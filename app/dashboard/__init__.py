from flask import Blueprint
from flask_restful import Api

dashboard_bp = Blueprint('dashboard',__name__, template_folder='templates')
api = Api(dashboard_bp)

from . import routes
from .api_routes import TaskListResource

api.add_resource(TaskListResource, "/api/tasks", "/api/tasks/<int:task_id>")