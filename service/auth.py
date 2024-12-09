from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from domain.sqlAlchemy.configuration import SessionLocal
from domain.sqlAlchemy.model.user_model import User
from domain.sqlAlchemy.repository.base_repository import BaseRepository
from typing import List, Dict, Any
from utils import utils
import logging


class AuthService:
    def __init__(self):
        self.db = SessionLocal()
        self.User = User
        self.user_repo = BaseRepository(self.User, self.db)
        
    def login_user(self, user_login: Dict[str, Any])-> dict[str, Any]:
        try:
            self.User.validation(user_login)

            user = self.user_repo.find_by(filters={"email": user_login.get("email")})

            if user is None or not check_password_hash(user.password, user_login.get("password")):
                return utils.json_response(401, "Invalid Email or Password", log_level="error")
            
            middleware_data = {"user_id": user.id, "email": user.email, "name": user.name}
            return utils.json_response(200, "Login Successfully!", middleware_data)
        except ValueError as ve:
            logging.error(f"Validation error while creating products: {str(ve)}")
            return utils.json_response(400, f"Validation Error: {str(ve)}", log_level="error")
        except Exception as e:
            return utils.json_response(500, "Internal Server Error", log_level="error")


    def register_user(self, user_register: Dict[str, Any]):
        try:
            self.User.validation(user_register)
            is_user = self.user_repo.find_by(filters={"email": user_register.get("email")}, columns=["id"])
            if is_user:
                return utils.json_response(400, "Email already exists", log_level="error")

            try:
                trx = self.user_repo.begin()
                created_products = self.user_repo.create(user_register)
                response = [self.User.to_dict(product) for product in created_products]
                self.user_repo.commit(trx=trx)
            except Exception as e:
                self.user_repo.rollback(trx=trx)
                return utils.json_response(500, f"Validation Error: {str(e)}", log_level="error")
            return utils.json_response(
                201,
                "Products created successfully!",
                response
            )
        except Exception as e:
            return utils.json_response(500, "Internal Server Error", log_level="error")


    def get_user_info(self, mdw: Dict[str, Any]):
        try:
            user_id = mdw.get('user_id')

            if not user_id:
                return utils.json_response(401, "User not found in token", log_level="error")
            
            user = self.user_repo.get_by_id(user_id, fields=["name", "email"])
            if not user:
                return utils.json_response(404, "User not found", log_level="error")

            response = self.User.to_dict(user)
            return utils.json_response(200, "Get User Successfully!", response)


        except Exception as e:
            return utils.json_response(500, "Internal Server Error", log_level="error")


    # def logout_user():
    #     try:
    #         # Mendapatkan token yang sedang digunakan
    #         # token = get_jwt_header()['Authorization'].split("Bearer ")[1]

    #         # Blacklist token di Redis (set token ke Redis dengan waktu kedaluwarsa)
    #         # r.setex(f"blacklisted:{token}", timedelta(minutes=15), "blacklisted")
    #         # # Jika menggunakan session atau cookie untuk token, bisa dihapus di sini (contoh menggunakan Flask session)
    #         # session.pop('access_token', None)  # jika menggunakan Flask session
    #         # # atau jika menggunakan cookie
    #         # response = jsonify({"message": "Logout successful"})
    #         # response.delete_cookie('access_token')  # jika menggunakan cookie
    #         # return response
            
    #         return utils.json_response(200, "Logout successful")
        
    #     except Exception as e:
    #         return utils.json_response(500, "Internal Server Error", log_level="error")


    # def refresh_token():
    #     # Menghasilkan access token baru menggunakan refresh token
    #     # current_user = get_jwt_identity()
    #     # new_access_token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=15))
    #     return {"access_token": "new_access_token"}