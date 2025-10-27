import pytest
from flask import url_for
from flask_jwt_extended import create_access_token
from app.models import User, Task
from app.extensions import db

@pytest.fixture
def setup_user_with_token(db):
    """
    Create a user in the test DB and yield a dict containing the user and
    a valid access token for that user. Clean up afterwards.
    """
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))

    return {"user":user, "access_token":access_token}


def test_get_tasks_emptylist(client, setup_user_with_token):
    """
    Authenticated GET to /dashboard/api/tasks should return 200 and an empty
    tasks list for a fresh user (no tasks created yet).
    """
    access_token = setup_user_with_token["access_token"]

    response = client.get(
        url_for("dashboard.tasklistresource"),
        headers={ "Authorization": f"Bearer {access_token}"}
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "Tasks fetched successfully" in data["message"]
    assert "tasks" in data["data"]
    assert isinstance(data["data"]["tasks"],list)
    assert len(data["data"]["tasks"]) == 0
    # Pagination metadata should exist (page, pages, total_tasks)
    assert "page" in data["data"]
    assert "pages" in data["data"]
    assert "total_tasks" in data["data"]
    assert data["data"]["total_tasks"] == 0

def test_create_task_success(client, setup_user_with_token):
    """
    Test creating a new task (POST /dashboard/api/tasks)
    """
    user = setup_user_with_token["user"]
    access_token = setup_user_with_token["access_token"]
    payload = {
        "title": "Buy groceries",
        "done": False
    }

    response = client.post(
        url_for("dashboard.tasklistresource"),
        headers={ "Authorization": f"Bearer {access_token}"},
        json=payload
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["status"] == "success"
    assert "Task created successfully" in data["message"]
    assert data["data"]["title"] == "Buy groceries"
    assert data["data"]["done"] is False

    task = Task.query.filter_by(title="Buy groceries", user_id=user.id).first()
    assert task is not None

def test_create_task_missing_title(client, setup_user_with_token):
    """
    Test creating a task without any title should return error (HTTP 400)
    """
    access_token = setup_user_with_token["access_token"]
    payload = {
        "done": False
    }

    response = client.post(
        url_for("dashboard.tasklistresource"),
        headers = { "Authorization": f"Bearer {access_token}"},
        json = payload
    )
    data = response.get_json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Title is required" in data["message"]

def test_update_task_success(client, setup_user_with_token):
    """Test updating an existing task (PUT /dashboard/api/tasks/<int:id>)"""
    user = setup_user_with_token["user"]
    access_token = setup_user_with_token["access_token"]
    task = Task(title="Old Title", done=False, user_id=user.id)
    db.session.add(task)
    db.session.commit()
    task_id = task.id

    payload = {
        "title": "Updated title",
        "done": True
    }

    response = client.put(
        url_for("dashboard.tasklistresource",task_id=task_id),
        headers={"Authorization": f"Bearer {access_token}"},
        json=payload
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "Task updated successfully" in data["message"]
    assert data["data"]["title"] == "Updated title"
    assert data["data"]["done"] is True

    updated_task = Task.query.filter_by(id=task_id,user_id=user.id).first()
    assert updated_task is not None
    assert updated_task.title == "Updated title"
    assert updated_task.done is True

def test_update_task_not_found(client, setup_user_with_token):
    """
    Trying to update a non-existent task should return 404.
    """
    user = setup_user_with_token["user"]
    access_token = setup_user_with_token["access_token"]

    invalid_task_id = 65465
    payload = {
        "title": "Does not exist",
        "done": True
    }

    response = client.put(
        url_for("dashboard.tasklistresource",task_id=invalid_task_id),
        headers={"Authorization": f"Bearer {access_token}"},
        json=payload
    )
    data = response.get_json()

    assert response.status_code == 404
    assert data["status"] == "error"
    assert f"Task with task ID: {invalid_task_id} not found or unauthorized" in data["message"]

def test_delete_task_success(client, setup_user_with_token):
    """Test deleting an existing task (DELETE /dashboard/api/tasks/<int:id>)"""
    user = setup_user_with_token["user"]
    access_token = setup_user_with_token['access_token']

    task = Task(title="Task Title",done=False,user_id=user.id)
    db.session.add(task)
    db.session.commit()

    task_id = task.id

    response = client.delete(
        url_for("dashboard.tasklistresource",task_id=task_id),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert f"Task with task ID: {task_id} deleted successfully" in data["message"]
    assert data["data"]["title"] == "Task Title"
    assert data["data"]["done"] is False

    deleted_task = Task.query.filter_by(id=task_id,user_id=user.id).first()
    assert deleted_task is None

def test_delete_task_unauthorized_user(client, db):
    """Test that a user cannot delete another user's task"""
    # Create two users
    user1 = User(username="user1")
    user1.set_password("pass1")
    user2 = User(username="user2")
    user2.set_password("pass2")

    db.session.add_all([user1,user2])
    db.session.commit()

    # Create a task for user1
    task = Task(title="User1's Task",done=False,user_id=user1.id)
    db.session.add(task)
    db.session.commit()

    # Generate token for user2 (different user)
    access_token_user2 = create_access_token(identity=str(user2.id))

    # Try deleting user1's task with user2's token
    response = client.delete(
        url_for("dashboard.tasklistresource",task_id=task.id),
        headers={"Authorization": f"Bearer {access_token_user2}"},
    )
    data = response.get_json()

    assert response.status_code == 404
    assert data["status"] == "error"
    assert f"not found or unauthorized" in data["message"]
    
    task_still_exists = Task.query.filter_by(id=task.id,user_id=user1.id).first()
    assert task_still_exists is not None