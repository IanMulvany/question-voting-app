import pytest
from flask import url_for
from flask_socketio import SocketIOTestClient
from main import app, db, Idea, socketio  # Import the socketio instance


def test_home_page(client):
    """Test the home page is accessible."""
    response = client.get(url_for("home"))
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_vote_page(client):
    """Test the vote page is accessible."""
    response = client.get(url_for("vote"))
    assert response.status_code == 200
    assert b"Vote" in response.data  # Assuming the page contains "Vote"


def test_questions_page(client):
    """Test the questions page is accessible."""
    response = client.get(url_for("questions"))
    assert response.status_code == 200
    assert b"Questions" in response.data  # Assuming the page contains "Questions"


def test_submit_question_page(client):
    """Test the submit question page is accessible."""
    response = client.get(url_for("submit_question"))
    assert response.status_code == 200
    assert (
        b"Submit Question" in response.data
    )  # Assuming the page contains "Submit Question"


def test_admin_page(client):
    """Test the admin page is accessible."""
    response = client.get(url_for("admin"))
    assert response.status_code == 200
    assert b"Admin" in response.data  # Assuming the page contains "Admin"


def test_setup_test_data(client, session):
    """Test that the setup test data has been added to the database."""
    # Query the database for the test ideas
    idea1 = session.query(Idea).filter_by(title="Test Idea 1").first()
    idea2 = session.query(Idea).filter_by(title="Test Idea 2").first()

    # Assert that the ideas exist in the database
    assert idea1 is not None
    assert idea1.description == "Description for test idea 1"

    assert idea2 is not None
    assert idea2.description == "Description for test idea 2"


@pytest.fixture
def socket_client(test_app):
    """Create a Socket.IO test client."""
    socketio_client = SocketIOTestClient(socketio, app)  # Pass the socketio instance
    return socketio_client


def test_submit_question_via_socket(socket_client, session):
    """Test submitting a question via Socket.IO."""
    # Define the question data
    question_data = {
        "title": "Test Question",
        "description": "This is a test question via socket.",
    }

    # Emit the 'submit_idea' event with the question data
    socket_client.emit("submit_idea", question_data)

    # Check if the question was added to the database
    question = session.query(Idea).filter_by(title="Test Question").first()
    assert question is not None
    assert question.description == "This is a test question via socket."
