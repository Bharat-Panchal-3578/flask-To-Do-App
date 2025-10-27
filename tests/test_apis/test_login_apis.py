import pytest
from flask import url_for
from app.models import User
from app.extensions import db

@pytest.fixture
def setup_user(db):
    """Create a test user for login tests."""
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    return user
def test_login_success(client, setup_user):
    """Login with correct credentails should return 200 and tokens."""
    payload = {
        "username": "test_user",
        "password": "test_password"
    }

    response = client.post(url_for("auth.loginresource"),json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]

def test_login_missing_fields(client, setup_user):
    """Login with missing username/password returns 400."""
    payload = {
        "username": "test_user"
    }

    response = client.post(url_for("auth.loginresource"),json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Missing username or password" in data["message"]

def test_login_invalid_password(client, setup_user):
    """Login with incorrect password should return 401."""
    payload = {
        "username": "test_user",
        "password": "wrong_password"
    }

    response = client.post(url_for("auth.loginresource"),json=payload)
    data = response.get_json()

    assert response.status_code == 401
    assert data["status"] == "error"
    assert "Invalid username or password" in data["message"]


def test_login_nonexistent_user(client, setup_user):
    "Login with non-existing username should return 401."
    payload = {
        "username": "user",
        "password": "password"
    }

    response = client.post(url_for("auth.loginresource"),json=payload)
    data = response.get_json()

    assert response.status_code == 401
    assert data["status"] == "error"
    assert "Invalid username or password" in data["message"]