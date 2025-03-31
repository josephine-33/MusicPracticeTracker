from flask import Flask
from routes.auth_routes import auth_routes
from routes.session_routes import session_routes

app = Flask(__name__)

app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(session_routes, url_prefix="/api")

@app.route('/')
def home():
    return {"message": "Welcome to the MPT API!"}

if __name__ == '__main__':
    app.run(debug=True)
