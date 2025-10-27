import pytest
from datetime import datetime
from app.models import BlackListedToken
from app.extensions import db
from uuid import uuid4

def test_create_blacklisted_token(app, db):
    """Ensure a BlackListedToken can be created and stored correctly."""
    token_str = f"test_refresh_token_12345{uuid4()}" # unique every run
    token = BlackListedToken(token=token_str)
    db.session.add(token)
    db.session.commit()

    saved = BlackListedToken.query.filter_by(token=token_str).first()
    assert saved is not None
    assert saved.token == token_str
    assert isinstance(saved.blacklisted_on, datetime)