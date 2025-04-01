import pytest
import sqlite3
import json
from app import app

@pytest.fixture
def client():
    """Set up a test client for Flask"""
    app.config["TESTING"] = True
    client = app.test_client()

    # Set up test database
    with sqlite3.connect("instance/test_practice_sessions.db") as conn:
        # conn.execute("DELETE FROM users")
        # conn.execute("DELETE FROM practice_sessions")
        conn.commit()

    yield client

def test_register_user(client):
    """Test user registration."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201