import pytest
import csv
import io
from flask import url_for
from flask_socketio import SocketIOTestClient, join_room, leave_room
from main import app, db, Idea, socketio  # Import the socketio instance


def test_home_page(client):
    """Test the home page is accessible and contains expected elements."""
    response = client.get(url_for("home"))
    assert response.status_code == 200
    assert b"QuestionVote" in response.data
    assert b"Ask Questions, Get Answers, Make Decisions" in response.data
    assert b"How It Works" in response.data
    assert b"Submit Questions" in response.data
    assert b"Vote on Questions" in response.data
    assert b"View Results" in response.data


def test_vote_page(client):
    """Test the vote page is accessible and contains expected elements."""
    response = client.get(url_for("vote"))
    assert response.status_code == 200
    assert b"Vote on Questions" in response.data
    assert b"Help prioritize questions" in response.data
    assert b"QuestionVote" in response.data
    
    # Check for voting container and loading elements
    assert b'id="ideas-container"' in response.data
    assert b'id="loader"' in response.data
    assert b'class="loader-spinner"' in response.data


def test_questions_page(client):
    """Test the questions page is accessible."""
    response = client.get(url_for("questions"))
    assert response.status_code == 200
    assert b"Submitted Questions" in response.data
    assert b"Sort by Latest" in response.data
    assert b"Sort by Votes" in response.data


def test_questions_sorting(client, test_app):
    """Test sorting functionality on the questions page."""
    with test_app.app_context():
        # Clear existing data
        db.session.query(Idea).delete()
        db.session.commit()
        
        # Add ideas with different vote counts
        idea1 = Idea(title="Low votes question", description="This has few votes")
        idea1.votes = 2
        
        idea2 = Idea(title="High votes question", description="This has many votes")
        idea2.votes = 15
        
        idea3 = Idea(title="Medium votes question", description="This has some votes")
        idea3.votes = 7
        
        db.session.add_all([idea1, idea2, idea3])
        db.session.commit()
        
        # Test default sorting (by date/ID)
        response = client.get(url_for("questions"))
        assert response.status_code == 200
        assert b"Sort by Latest" in response.data
        content = response.data.decode('utf-8')
        
        # Check that the latest idea (idea3) is listed first in the HTML
        # This is an approximate test since we're just checking the order in the HTML
        idea3_pos = content.find("Medium votes question")
        idea2_pos = content.find("High votes question")
        idea1_pos = content.find("Low votes question")
        assert idea3_pos < idea2_pos < idea1_pos
        
        # Test sorting by votes
        response = client.get(url_for("questions", sort="votes"))
        assert response.status_code == 200
        assert b"Sort by Votes" in response.data
        content = response.data.decode('utf-8')
        
        # Check that the highest voted idea (idea2) is listed first in the HTML
        idea2_pos = content.find("High votes question")
        idea3_pos = content.find("Medium votes question")
        idea1_pos = content.find("Low votes question")
        assert idea2_pos < idea3_pos < idea1_pos


def test_submit_question_page(client):
    """Test the submit question page is accessible and properly structured."""
    response = client.get(url_for("submit_question"))
    assert response.status_code == 200
    assert b"Submit Your Question" in response.data
    
    # Check for form elements
    assert b'id="question-input"' in response.data
    assert b'id="submit-question"' in response.data
    
    # Check success container starts hidden
    assert b'id="success-container" class="success-container"' in response.data
    assert b'display: none' in response.data
    
    # Check for navigation options
    assert b'View All Questions' in response.data
    assert b'Vote on Questions' in response.data


def test_admin_page(client):
    """Test the admin page is accessible."""
    response = client.get(url_for("admin"))
    assert response.status_code == 200
    assert b"Admin Panel" in response.data
    assert b"Question Management" in response.data


def test_export_csv(client, test_app):
    """Test exporting questions to CSV."""
    with test_app.app_context():
        # Clear existing data
        db.session.query(Idea).delete()
        db.session.commit()
        
        # Add ideas to the database
        idea1 = Idea(title="Test CSV Idea 1", description="Description for CSV test 1")
        idea2 = Idea(title="Test CSV Idea 2", description="Description for CSV test 2")
        db.session.add(idea1)
        db.session.add(idea2)
        db.session.commit()
        
        # Request the CSV export
        response = client.get(url_for("export_csv"))
        
        # Check response
        assert response.status_code == 200
        assert response.mimetype == "text/csv"
        assert "attachment" in response.headers["Content-Disposition"]
        assert "questions-" in response.headers["Content-Disposition"]
        
        # Parse CSV content
        csv_data = response.data.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(csv_data))
        rows = list(csv_reader)
        
        # Check CSV structure
        assert len(rows) == 3  # Header + 2 ideas
        assert rows[0] == ['ID', 'Title', 'Description', 'Votes']
        
        # Check data (sort by title to ensure consistent test results)
        data_rows = sorted(rows[1:], key=lambda row: row[1])
        assert "Test CSV Idea 1" in data_rows[0][1]
        assert "Description for CSV test 1" in data_rows[0][2]
        assert "Test CSV Idea 2" in data_rows[1][1]
        assert "Description for CSV test 2" in data_rows[1][2]


def test_clear_questions(client, test_app):
    """Test clearing all questions."""
    with test_app.app_context():
        # Clear existing data
        db.session.query(Idea).delete()
        db.session.commit()
        
        # Add ideas to the database
        idea1 = Idea(title="Test Clear Idea 1", description="Description for clear test 1")
        idea2 = Idea(title="Test Clear Idea 2", description="Description for clear test 2")
        db.session.add(idea1)
        db.session.add(idea2)
        db.session.commit()
        
        # Verify ideas exist
        assert db.session.query(Idea).count() == 2
        
        # Send request to clear questions
        response = client.post(url_for("clear_questions"))
        
        # Check response
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        
        # Verify ideas are deleted
        assert db.session.query(Idea).count() == 0


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
    client = test_app.test_client()
    socketio_client = socketio.test_client(test_app, flask_test_client=client)
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


def test_vote_functionality(socket_client, session, test_app):
    """Test the vote functionality via Socket.IO."""
    # Create a test question
    with test_app.app_context():
        idea = Idea(title="Voting Test Question", description="This is for testing votes")
        session.add(idea)
        session.commit()
        idea_id = idea.id
    
    # Test initial votes
    question = session.get(Idea, idea_id)
    assert question.votes == 0
    
    # Test clicking upvote button multiple times
    # First upvote
    socket_client.emit("vote", {"id": idea_id, "change": 1})
    socket_client.get_received()  # Clear received events
    
    # Check the vote count is incremented
    question = session.get(Idea, idea_id)
    assert question.votes == 1
    
    # Second upvote
    socket_client.emit("vote", {"id": idea_id, "change": 1})
    socket_client.get_received()
    
    # Check the vote count is incremented again
    question = session.get(Idea, idea_id)
    assert question.votes == 2
    
    # Test clicking downvote button
    socket_client.emit("vote", {"id": idea_id, "change": -1})
    socket_client.get_received()
    
    # Check the vote count is decremented
    question = session.get(Idea, idea_id)
    assert question.votes == 1
    
    # Multiple downvotes
    socket_client.emit("vote", {"id": idea_id, "change": -1})
    socket_client.get_received()
    question = session.get(Idea, idea_id)
    assert question.votes == 0
    
    socket_client.emit("vote", {"id": idea_id, "change": -1})
    socket_client.get_received()
    question = session.get(Idea, idea_id)
    assert question.votes == -1
    
    # Mix of upvotes and downvotes
    socket_client.emit("vote", {"id": idea_id, "change": 1})
    socket_client.get_received()
    question = session.get(Idea, idea_id)
    assert question.votes == 0
    
    socket_client.emit("vote", {"id": idea_id, "change": 1})
    socket_client.get_received()
    question = session.get(Idea, idea_id)
    assert question.votes == 1
