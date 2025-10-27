import pytest
from app.models import User, Task
from app.extensions import db

@pytest.fixture
def setup_user(app):
    """Create a clean database before each test."""
    db.drop_all()
    db.create_all()

    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    yield user

    db.session.remove()
    db.drop_all()

def test_task_to_dict_returns_correct_fields(app, setup_user):
    """Ensure Task.to_dict() returns correct fields"""
    user = setup_user
    task = Task(title="Test Task",done=False,user_id=user.id)
    db.session.add(task)
    db.session.commit()

    task_dict = task.to_dict()

    assert set(task_dict.keys()) == {'id','title','done','user_id'}
    assert task_dict["title"] == "Test Task"
    assert task_dict["done"] is False
    assert task_dict["user_id"] == user.id

def test_task_belongs_to_user(app, setup_user):
    """Ensure task is correctly linked to user via relationship."""
    user = setup_user
    task = Task(title="Test Task",done=False,user_id=user.id)
    db.session.add(task)
    db.session.commit()

    # Re-fetch both fresh from DB
    fresh_user = User.query.filter_by(id=user.id).first()
    fresh_task = Task.query.filter_by(id=task.id).first()

    assert fresh_task.user_id == fresh_user.id
    assert fresh_task.user.username == "test_user"
    assert len(fresh_user.tasks) == 1
    assert fresh_user.tasks[0].title == "Test Task"