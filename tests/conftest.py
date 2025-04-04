import pytest
from app import app as flask_app
import sqlite3

@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    client = app.test_client()

    # clear database for testing
    with sqlite3.connect("instance/test_practice_sessions.db") as conn:
        conn.execute("DELETE FROM users")
        conn.execute("DELETE FROM practice_sessions")
        conn.commit()

    return client