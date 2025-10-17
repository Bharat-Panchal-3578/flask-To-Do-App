from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task
from app.extensions import db
from app.utils import success_response, error_response

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        pass

    @jwt_required()
    def post(self):
        pass

    @jwt_required()
    def put(self):
        pass

    @jwt_required()
    def delete(self):
        pass