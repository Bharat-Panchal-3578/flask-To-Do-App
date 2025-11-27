import pytest
from datetime import datetime
from app.models import BlackListedToken
from app.extensions import db
from uuid import uuid4

def test_create_blacklisted_token(app, db):
    """Ensure a BlackListedToken can be created and stored correctly."""
    jti_str = "dummy_jti_12345"
    token = BlackListedToken(jti=jti_str)
    db.session.add(token)
    db.session.commit()

    saved = BlackListedToken.query.filter_by(jti=jti_str).first()
    assert saved is not None
    assert saved.jti == jti_str
    assert isinstance(saved.blacklisted_on, datetime)