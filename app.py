from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from practice_sessions import (
    insert_practice_session,
    get_all_user_practice_sessions,
    get_practice_session,
    update_practice_session,
    delete_practice_session
)


app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('practice_sessions.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the MPT API!"})


# add a practice session
@app.route('/practice_sessions', methods=['POST'])
def add_practice_sessions():
    data = request.json
    user_id = data.get('user_id')
    piece = data.get('piece')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    notes = data.get('notes')
    instrument = data.get('instrument')

    if not all([user_id, piece, date, start_time, end_time, instrument]):
        return jsonify({"error": "Missing required fields"}), 400

    insert_practice_session(user_id, piece, date, start_time, end_time, notes, instrument)
    return jsonify({"message": "Practice session added successfully!"}), 201    


# get all practice sessions for a user
@app.route('/practice_sessions/<int:user_id>', methods=['GET'])
def fetch_user_sessions(user_id):
    sessions = get_all_user_practice_sessions(user_id)
    
    if not sessions:
        return jsonify({"message": "No practice sessions found"}), 404

    return jsonify(sessions)


# get a specific practice session
@app.route('/practice_sessions/<int:session_id>', methods=['GET'])
def fetch_practice_session(session_id):
    session = get_practice_session(session_id)

    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify(session)


# update existing practice session
@app.route('/practice_sessions/<int:session_id>', methods=['PUT'])
def modify_practice_session(session_id):
    data = request.json
    update_practice_session(session_id,
        piece=data.get('piece'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        notes=data.get('notes'),
        instrument=data.get('instrument')
    )

    return jsonify({"message": "Practice session updated successfully!"})


# delete a practice session
@app.route('/practice_sessions/<int:session_id>', methods=['DELETE'])
def remove_practice_session(session_id):
    delete_practice_session(session_id)
    return jsonify({"message": "Practice session deleted successfully!"})