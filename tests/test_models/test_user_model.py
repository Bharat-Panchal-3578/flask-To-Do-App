import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.extensions import db

@pytest.fixture
def clean_db(app):
    """Create a clean database before each test."""
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()

def test_set_password_hashes_correctly(app, clean_db):
    """Ensure password is hashed and not stored as plain text."""
    user = User(username="test_user")
    user.set_password("test_password")

    # pdkdf2... -> Used via flask for hashing, scrypt... -> Used via Werkzeug
    assert user.password_hash != "test_password"
    assert any(user.password_hash.startswith(prefix) for prefix in ["pbkdf2:", "scrypt:"])

def test_check_password_valid(app, clean_db):
    """Ensure check_password returns True for correct password."""
    user = User(username="test_user")
    user.set_password("test_password")

    db.session.add(user)
    db.session.commit()

    assert user.check_password("test_password") is True

def test_check_password_invalid(app, clean_db):
    """Ensure check_password returns False for wrong password."""
    user = User(username="test_user")
    user.set_password("test_password")

    db.session.add(user)
    db.session.commit()

    assert user.check_password("wrong Password") is False

def test_username_unique_constraint(app, clean_db):
    """Ensure username uniqueness constraint works."""
    user1 = User(username="test_user")
    user1.set_password("password1")

    db.session.add(user1)
    db.session.commit()

    user2 = User(username="test_user")
    user2.set_password("password2")
    db.session.add(user2)

    # Type of SQL constraint violation, throwing when unique constraint is not followed
    with pytest.raises(IntegrityError):
        db.session.commit()