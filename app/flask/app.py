from flask import Flask
from app.flask.routes.router import router
from flask_jwt_extended import JWTManager
from app.flask.routes.product import product_router


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "your_secret_key"  
    
    jwt = JWTManager(app)
    app.register_blueprint(router)
    app.register_blueprint(product_router)

    return app
