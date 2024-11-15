import sys
import os

# Add the parent directory of 'tests' to the Python path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

# Set test database URL before importing the app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from main import app, db, Idea  # Import the app, db, and Idea from main.py


@pytest.fixture(scope="session", autouse=True)
def prevent_live_db_access():
    """Prevent tests from running if DATABASE_URL points to a live database."""
    db_url = os.environ.get("DATABASE_URL", "")
    if "prod" in db_url:  # Replace with an identifier specific to your live DB
        raise RuntimeError(
            f"Tests are attempting to run against a live database: {db_url}. Abort!"
        )


@pytest.fixture(scope="function")
def test_app():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SERVER_NAME"] = "localhost"

    db_url = os.environ.get("DATABASE_URL", "")
    if "prod" in db_url:  # Replace with an identifier specific to your live DB
        raise RuntimeError(
            f"Tests are attempting to run against a live database: {db_url}. Abort!"
        )

    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_test_data(test_app):  # test app is defined to use sqlite://:memory
    with test_app.app_context():
        # Create some test data
        idea1 = Idea(title="Test Idea 1", description="Description for test idea 1")
        idea2 = Idea(title="Test Idea 2", description="Description for test idea 2")
        db.session.add(idea1)
        db.session.add(idea2)
        db.session.commit()


@pytest.fixture(scope="function")
def client(
    test_app, setup_test_data
):  # test app is defined to use sqlite://:memory and to add test data
    with test_app.app_context():
        db.create_all()
        client = test_app.test_client()
        yield client  # client is made available to the test

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
