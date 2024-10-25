import pytest
from flask import url_for


def test_home_page(client):
    """Test the home page is accessible."""
    response = client.get(url_for('home'))
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_vote_page(client):
    """Test the vote page is accessible."""
    response = client.get(url_for('vote'))
    assert response.status_code == 200
    assert b"Vote" in response.data  # Assuming the page contains "Vote"

def test_questions_page(client):
    """Test the questions page is accessible."""
    response = client.get(url_for('questions'))
    assert response.status_code == 200
    assert b"Questions" in response.data  # Assuming the page contains "Questions"

def test_submit_question_page(client):
    """Test the submit question page is accessible."""
    response = client.get(url_for('submit_question'))
    assert response.status_code == 200
    assert b"Submit Question" in response.data  # Assuming the page contains "Submit Question"

def test_admin_page(client):
    """Test the admin page is accessible."""
    response = client.get(url_for('admin'))
    assert response.status_code == 200
    assert b"Admin" in response.data  # Assuming the page contains "Admin"

def test_idea_creation(client, session):
    """Test creating a new idea."""
    response = client.post(
        url_for("submit_idea"),
        data={"title": "New Idea", "description": "This is a test idea."},
    )
    assert response.status_code == 302  # Assuming a redirect after creation

    # Verify the idea is in the database
    from llm_comparison_app.models.idea import Idea

    idea = session.query(Idea).filter_by(title="New Idea").first()
    assert idea is not None
    assert idea.description == "This is a test idea."
