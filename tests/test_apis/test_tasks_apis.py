import pytest
from flask import url_for
from flask_jwt_extended import create_access_token
from app.models import User, Task
from app.extensions import db

@pytest.fixture
def setup_user_with_token(app):
    """
    Create a user in the test DB and yield a dict containing the user and
    a valid access token for that user. Clean up afterwards.
    """
    db.drop_all()
    db.create_all()

    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))

    yield {"user":user, "access_token":access_token}

    db.session.remove()
    db.drop_all()

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

def test_create_task_success(client,app, setup_user_with_token):
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

    with app.app_context():
        task = Task.query.filter_by(title="Buy groceries", user_id=user.id).first()
        assert task is not None