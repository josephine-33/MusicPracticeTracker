from flask import Blueprint, request, jsonify
from utils.security import get_user_from_token
from models.practice import (
    insert_practice_session,
    get_all_user_practice_sessions,
    get_practice_session,
    update_practice_session,
    delete_practice_session,
)
import jwt

session_routes = Blueprint("session_routes", __name__)

SECRET_KEY = "your_secret_key"

def get_user_from_token():
    """Extract user ID from the token in the Authorization header."""
    token = request.headers.get("Authorization")
    
    if not token:
        return None
    
    try:
        token = token.split(" ")[1]  # Remove "Bearer "
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data["user_id"]
    except:
        return None

@session_routes.route("/practice_sessions", methods=["POST"])
def add_practice_sessions():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}, 401)
    
    data = request.json
    if not all([data.get("piece"), data.get("date"), data.get("start_time"), data.get("end_time"), data.get("instrument")]):
        return jsonify({"error": "Missing required fields"}), 400
    
    insert_practice_session(user_id, **data)
    return jsonify({"message": "Practice session added successfully!"}), 201

@session_routes.route("/practice_sessions", methods=["GET"])
def fetch_user_session():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}, 401)
    
    sessions = get_all_user_practice_sessions(user_id)
    if not sessions:
        return jsonify({"error": "No practice sessions found"}), 404

    return jsonify(sessions)

@session_routes.route("/practice_sessions/<int:session_id>", methods=["GET"])
def fetch_practice_session(session_id):
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = get_practice_session(session_id)
    if not session:
        return jsonify({"error": "No practice session found"}), 404
    if session["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    return jsonify(session)

@session_routes.route("/practice_sessions/<int:session_id>", methods=["PUT"])
def modify_practice_session(session_id):
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}, 401)
    
    session = get_practice_session(session_id)
    if not session:
        return jsonify({"error": "No practice session found"}), 404
    if session["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 401
    

    data = request.json
    update_practice_session(session_id, **data)
    return jsonify({"message": "Practice session updated successfully!"})

@session_routes.route("/practice_sessions/<int:session_id>", methods=["DELETE"])
def remove_practice_session(session_id):
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}, 401)
    
    session = get_practice_session(session_id)
    if not session:
        return jsonify({"error": "No practice session found"}), 404
    if session["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    delete_practice_session(session_id)
    return jsonify({"message": "Practice session deleted successfully!"})