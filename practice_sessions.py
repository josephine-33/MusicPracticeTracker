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

def insert_practice_session(user_id, piece, date, start_time, end_time, notes):
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
        INSERT INTO practice_sessions (user_id, piece, date, start_time, end_time, duration, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, piece, date, start_time, end_time, duration, notes))

    # Commit and close connection
    connection.commit()
    connection.close()

