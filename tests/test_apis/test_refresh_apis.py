import pytest
from flask import url_for
from flask_jwt_extended import create_refresh_token
from app.extensions import db
from app.models import User

@pytest.fixture
def setup_user_with_token(db):
    """Create a user and generate a refresh token."""
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    refresh_token = create_refresh_token(identity=str(user.id))
    return user, refresh_token

def test_refresh_success(client, setup_user_with_token):
    """POST /api/refresh with valid refresh token should return new access token."""
    _, refresh_token = setup_user_with_token

    response = client.post(
        url_for("auth.refreshtokenresource"),
        headers = {"Authorization": f"Bearer {refresh_token}"}
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "access_token" in data["data"]

def test_refresh_token_missing_header(client):
    """POST /api/refresh without Authorization header should fail."""
    response = client.post(url_for("auth.refreshtokenresource"))

    assert response.status_code in [401, 422]

def test_refresh_token_with_blacklisted_token(client, db, setup_user_with_token):
    """POST /api/refresh with blacklisted token should fail and return 401 """
    user, refresh_token = setup_user_with_token

    # Logout to blacklist token
    client.post(url_for("auth.logoutresource"),json={"refresh_token": refresh_token})

    # Try to refresh with same token
    response = client.post(
        url_for("auth.refreshtokenresource"),
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    data = response.get_json()

    assert response.status_code == 401
    assert data["status"] == "error"
    assert "Token has been revoked" in data["message"]