from flask import Flask
from app.flask.routes.router import router
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "your_secret_key"  
    
    jwt = JWTManager(app)
    app.register_blueprint(router)

    return app
