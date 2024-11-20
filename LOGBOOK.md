# 2024-10-28

When I run the test suite, the live db is deleted. I had this with the other flask app that I created, so I need to figure out how to fix this by looking at the other app.

It looks like this is caused because main.py create app which hardcodes the uri to the live DB. 
If I:


app = Flask(__name__)

# Use environment variable for database URI, with a default for local development
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///ideas.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions with the app
db.init_app(app)
migrate.init_app(app, db)
socketio.init_app(app)

and then 

   export DATABASE_URL="sqlite:///path/to/your/live/ideas.db"

   it should work -> shold createa  new git repo for this. 


in conftest.py I can then do the following:

# tests/conftest.py
import os
import pytest

@pytest.fixture(scope='session', autouse=True)
def set_test_environment():
    """Set the environment variable for the test database."""
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'  # Use in-memory database for tests
    yield
    # Optionally, you can clean up or reset the environment variable after tests
    del os.environ['DATABASE_URL']


