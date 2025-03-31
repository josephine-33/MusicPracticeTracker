from flask import Blueprint, request, jsonify
import jwt
import datetime
import os
from models.users import create_user, authenticate_user

auth_routes = Blueprint("auth_routes", __name__)
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    if not all([data.get("username"), data.get("email"), data.get("password")]):
        return jsonify({"error": "Missing fields"}, 400)

    success = create_user(data["username"], data["email"], data["password"])
    if not success:
        return jsonify({"error": "User already exists"}), 400
    return jsonify({"message": "User registered successfully"}), 201


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = authenticate_user(data["email"], data["password"])

    if not user_id:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify({"token": token})
