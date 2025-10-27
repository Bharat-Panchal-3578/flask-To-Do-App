import pytest
from flask import url_for
from app.models import User
from app.extensions import db

def test_register_success(client, db):
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

    user = User.query.filter_by(username="test_user").first()
    assert user is not None

def test_register_missing_fields(client, db):
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

def test_register_duplicate_user(client, db):
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