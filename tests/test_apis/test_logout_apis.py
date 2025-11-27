import pytest
from flask import url_for
from flask_jwt_extended import create_refresh_token, decode_token
from app.models import BlackListedToken, User
from app.extensions import db

@pytest.fixture
def setup_user_with_token(db):
    """Create a user and generate a refresh token."""
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    refresh_token = create_refresh_token(identity=str(user.id))
    return user, refresh_token

def test_logout_success(client, db, setup_user_with_token):
    """
    POST /api/logout should blacklist the refresh token JTI and return 200.
    """
    user, refresh_token = setup_user_with_token

    response = client.post(
        url_for("auth.logoutresource"),
        json={"refresh_token": refresh_token}
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "Logged out successfully" in data["message"]

    # Check that JTI s in blacklist
    decoded = decode_token(refresh_token)
    jti = decoded["jti"]
    blacklisted = BlackListedToken.query.filter_by(jti=jti).first()
    assert blacklisted is not None

def test_logout_missing_token(client, db):
    """
    POST /api/logout without refresh_token should return 400.
    """
    response = client.post(url_for("auth.logoutresource"), json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["status"] == "error"
    assert "Refresh token is required" in data["message"]