import pytest
from app import create_app, db as _db
from app.models import User, Task

@pytest.fixture(scope='function')
def app():
    """Create and configure a new app instance for tests."""
    app = create_app("app.config.TestingConfig")
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def client(app):
    """A test client for sending HTTP requests."""
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    """Create the database tables and drop after testing."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()