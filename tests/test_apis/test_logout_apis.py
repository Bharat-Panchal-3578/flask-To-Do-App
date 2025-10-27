import pytest
from flask import url_for
from app.models import BlackListedToken
from app.extensions import db

def test_logout_success(client, db):
    """
    POST /api/logout with valid refresh_token should blacklist the token and return 200.
    """
    payload = {
        "refresh_token": "dummy_refresh_token_12345"
    }

    response = client.post(url_for("auth.logoutresource"),json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "Logged out successfully" in data["message"]

    blacklisted = BlackListedToken.query.filter_by(token="dummy_refresh_token_12345").first()
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