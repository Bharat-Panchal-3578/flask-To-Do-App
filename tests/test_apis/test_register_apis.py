import pytest
from flask import url_for
from app.models import User
from app.extensions import db

@pytest.fixture
def clean_db(app):
    """Cleans up DB before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_register_success(client, app, clean_db):
    """
    Test for user registration.
    """
    payload = {
        "username":"test_user",
        "password": "test_password"
    }

    response = client.post(
        url_for("auth.registerresource"),
        json=payload
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["status"] == "success"
    assert "username" in data["data"]
    assert data["data"]["username"] == "test_user"

    # Verify user is actually in DB
    with app.app_context():
        user = User.query.filter_by(username="test_user").first()
        assert user is not None

def test_register_missing_fields(client, app, clean_db):
    """
    Test registration with missing username/password returns 400.
    """
    payload = {
        "username": "test_user"
    }

    response = client.post(
        url_for("auth.registerresource"),
        json=payload
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Missing fields" in data["message"]

def test_register_duplicate_user(client, app, clean_db):
    """
    Test registration fails if username already exists.
    """
    payload = { "username": "test_user", "password": "test_password"}

    # First registration
    client.post(url_for("auth.registerresource"),json=payload)
    # Duplicate registration
    response = client.post(url_for("auth.registerresource"),json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Username already taken" in data["message"]