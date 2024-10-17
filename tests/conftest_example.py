import sys
import os

# Add the parent directory of 'tests' to the Python path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

import pytest
from llm_comparison_app import create_app, db
from llm_comparison_app.models.task_type import TaskType  # Import all your models here

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)


@pytest.fixture(scope="function")
def app():
    from llm_comparison_app.config import TestConfig

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    with app.app_context():
        db.create_all()
        print("Tables after create_all:", db.engine.table_names())  # Debug print

    client = app.test_client()

    yield client

    with app.app_context():
        print("Tables before drop_all:", db.engine.table_names())  # Debug print
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
