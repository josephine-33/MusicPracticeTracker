import sqlite3
from datetime import datetime

def insert_practice_session(user_id, piece, date, start_time, end_time, notes, instrument):
    # establishing connection
    connection = sqlite3.connect('instance/practice_sessions.db')
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

def get_all_user_practice_sessions(user_id):
    """Retrieving all practice sessions associated with given user_id."""
    # establishing connection
    connection = sqlite3.connect('instance/practice_sessions.db')
    cursor = connection.cursor()

    # getting sessions
    cursor.execute("SELECT * FROM practice_sessions WHERE user_id = ?", (user_id,))
    sessions = cursor.fetchall()

    # close and return array with all practice sessions
    connection.close()
    return sessions

def get_practice_session(session_id):
    connection = sqlite3.connect('instance/practice_sessions.db')
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute ("SELECT * FROM practice_sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    
    if not session:
        #TODO throw exception? is there a better way to see if the session exists?
        print("session not found")
        connection.close()
        return

    connection.close()
    return dict(session)

def update_practice_session(session_id, piece=None, start_time=None, end_time=None, notes=None, instrument=None):
    connection = sqlite3.connect('instance/practice_sessions.db')
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
    # date = date if date else session[1]
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
    connection = sqlite3.connect('instance/practice_sessions.db')
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