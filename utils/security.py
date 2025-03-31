from flask import request, jsonify
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Replace in production

def get_user_from_token():
    """Extract user ID from JWT token in Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or "Bearer " not in auth_header:
        return None

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
