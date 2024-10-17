import pytest
from flask import url_for

def test_home_page(client):
    """Test the home page is accessible."""
    response = client.get(url_for('home'))
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_idea_creation(client, session):
    """Test creating a new idea."""
    response = client.post(url_for('create_idea'), data={
        'title': 'New Idea',
        'description': 'This is a test idea.'
    })
    assert response.status_code == 302  # Assuming a redirect after creation

    # Verify the idea is in the database
    from llm_comparison_app.models.idea import Idea
    idea = session.query(Idea).filter_by(title='New Idea').first()
    assert idea is not None
    assert idea.description == 'This is a test idea.'
