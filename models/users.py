import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    connection = sqlite3.connect("instance/practice_sessions.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_user(username, email, password):
    """Creates a new user with a hashed password."""
    hashed_password = generate_password_hash(password)
    connection = get_db_connection()
    try:
        #TODO: see if these insert and find functions should be helper functions
        connection.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, hashed_password))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()

def authenticate_user(email, password):
    """Checks if given password matches the stored password hash."""
    connection = get_db_connection()
    user = connection.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    connection.close()

    if user and check_password_hash(user["password_hash"], password):
        return user["id"]
    return None