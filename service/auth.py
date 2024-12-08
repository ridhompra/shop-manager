from datetime import timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from domain.sqlAlchemy.configuration import SessionLocal
from domain.sqlAlchemy.model.user_model import User
from utils import utils


jwt = JWTManager()

def login_user(email: str, password: str):
    if not utils.validate_email(email):
        return utils.json_response(400, "Invalid Email format", log_level="error")

    if not utils.validate_password(password):
        return utils.json_response(400, "Password must be at least 6 characters, contain an uppercase letter and a number.", log_level="error")

    try:
        with SessionLocal() as session:
            user = session.query(User).filter_by(email=email).first()
        
        if user is None or not check_password_hash(user.password, password):
            return utils.json_response(401, "Invalid Email or Password", log_level="error")
        
        middlewareData = {"user_id": user.id, "email": user.email}

        # Generate JWT access token (valid selama 15 menit)
        access_token = create_access_token(identity=middlewareData, expires_delta=timedelta(minutes=15))
        
        return utils.json_response(200, "Login Successfully!", {"acces_token": access_token})

    except Exception as e:
        return utils.json_response(500, "Internal Server Error", log_level="error")

@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    user = SessionLocal().query(User).get(user_id)

    return {"user_id": user.id, "email": user.email}, 200
