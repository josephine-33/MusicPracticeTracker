import sqlite3
from datetime import datetime

# # Connect to SQLite database
# connection = sqlite3.connect('practice_sessions.db')
# cursor = connection.cursor()

# # Create the users table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE NOT NULL,
#         email TEXT UNIQUE NOT NULL,
#         password_hash TEXT NOT NULL
#     )
# """)

# # Create the practice_sessions table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS practice_sessions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         piece TEXT NOT NULL,
#         date TEXT NOT NULL,  -- Store as 'YYYY-MM-DD'
#         start_time TEXT NOT NULL,  -- Store as 'YYYY-MM-DD HH:MM:SS'
#         end_time TEXT NOT NULL,  -- Store as 'YYYY-MM-DD HH:MM:SS'
#         duration INTEGER NOT NULL,  -- Store duration in seconds
#         notes TEXT,
#         FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#     )
# """)

# adding instrument column
# connection = sqlite3.connect('practice_sessions.db')
# cursor = connection.cursor()

# # Add the new column if it doesn't exist
# cursor.execute("ALTER TABLE practice_sessions ADD COLUMN instrument TEXT")

# connection.commit()
# connection.close()

def insert_practice_session(user_id, piece, date, start_time, end_time, notes, instrument):
    # establishing connection
    connection = sqlite3.connect('practice_sessions.db')
    cursor = connection.cursor()

    # Convert string timestamps to datetime objects
    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    # Calculate duration in seconds
    duration = int((end_dt - start_dt).total_seconds()) #TODO: change this bc why tf would it be in seconds

    # insert
    cursor.execute("""
        INSERT INTO practice_sessions (user_id, piece, date, start_time, end_time, duration, notes, instrument)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, piece, date, start_time, end_time, duration, notes, instrument))

    # Commit and close connection
    connection.commit()
    connection.close()

def get_user_practice_sessions(user_id):
    """Retrieving all practice sessions associated with given user_id."""
    # establishing connection
    connection = sqlite3.connect('practice_sessions.db')
    cursor = connection.cursor()

    # getting sessions
    cursor.execute("SELECT * FROM practice_sessions WHERE user_id = ?", (user_id,))
    sessions = cursor.fetchall()

    # close and return array with all practice sessions
    connection.close()
    return sessions


def update_practice_session(session_id, piece=None, start_time=None, end_time=None, notes=None, instrument=None):
    connection = sqlite3.connect('practice_sessions.db')
    cursor = connection.cursor()

    cursor.execute ("SELECT * FROM practice_sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    # print(session)
    if not session:
        #TODO throw exception?
        print("session not found")
        connection.close()
        return

    # keep existing values if new ones aren't provided
    piece = piece if piece else session[2]
    start_time = start_time if start_time else session[4]
    end_time = end_time if end_time else session[5]
    notes = notes if notes else session[7]
    instrument = instrument if instrument else session[8]

    # calculate duration
    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    duration = int((end_dt - start_dt).total_seconds())

    cursor.execute("""
        UPDATE practice_sessions
        SET piece = ?, start_time = ?, end_time = ?, duration = ?, notes = ?, instrument = ?
        WHERE id = ?
        """, (piece, start_time, end_time, duration, notes, instrument, session_id))
    
    connection.commit()
    connection.close()

def delete_practice_session(session_id):
    connection = sqlite3.connect('practice_sessions.db')
    cursor = connection.cursor()

    cursor.execute ("SELECT * FROM practice_sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    
    if not session:
        #TODO throw exception? is there a better way to see if the session exists?
        print("session not found")
        connection.close()
        return

    # delete session
    cursor.execute("DELETE FROM practice_sessions WHERE id = ?", (session_id,))
    connection.commit()
    connection.close()

delete_practice_session(2)