import sys
import os

# Add the parent directory of 'tests' to the Python path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

import pytest
from main import app, db  # Import the app and db from main.py

@pytest.fixture(scope="function")
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(test_app):
    with test_app.app_context():
        db.create_all()

    client = test_app.test_client()

    yield client

    with test_app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def session(test_app):
    with test_app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
