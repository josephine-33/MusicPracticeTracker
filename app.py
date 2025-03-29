from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from routes.auth_routes import auth_routes
from routes.session_routes import session_routes

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Register blueprints (routes)
app.register_blueprint(auth_routes)
app.register_blueprint(session_routes)

if __name__ == "__main__":
    app.run(debug=True)
