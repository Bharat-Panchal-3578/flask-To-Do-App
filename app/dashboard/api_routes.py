from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task
from app.extensions import db
from app.utils import success_response, error_response

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())

        done_filter = request.args.get("done")
        page = request.args.get("page",1,type=int)
        limit = request.args.get("limit",5,type=int)
        
        query = Task.query.filter_by(user_id=current_user_id)

        if done_filter is not None:
            done = done_filter.lower() == 'true'
            query = query.filter_by(done=done)
        
        paginated = query.paginate(page=page,per_page=limit,error_out=False)

        data = {
            "tasks":[task.to_dict() for task in paginated.items],
            "page":paginated.page,
            "pages":paginated.pages,
            "total_tasks":paginated.total
        }

        return success_response(data=data, message="Tasks fetched successfully")

    @jwt_required()
    def post(self):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        title = data.get('title')
        done = data.get('done',False)
        
        if not title:
            return error_response("Title is required",400)

        new_task = Task(title=title,done=done,user_id=current_user_id)
        db.session.add(new_task)
        db.session.commit()
        
        return success_response(new_task.to_dict(),message="Task created successfully",status=201)

    @jwt_required()
    def put(self, task_id):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        task = Task.query.filter_by(id=task_id,user_id=current_user_id).first()

        if task is None:
            return error_response(f"Task with task ID: {task_id} not found or unauthorized")

        task.title = data.get('title',task.title)
        task.done = data.get('done',task.done)

        db.session.commit()

        return success_response(task.to_dict(),"Task updated successfully")

    @jwt_required()
    def delete(self, task_id):
        current_user_id = int(get_jwt_identity())

        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        if task is None:
            return error_response(f"Task with task ID: {task_id} not found or unauthorized")

        db.session.delete(task)
        db.session.commit()

        return success_response(
            data=task.to_dict(),
            message=f"Task with task ID: {task_id} deleted successfully"
        )