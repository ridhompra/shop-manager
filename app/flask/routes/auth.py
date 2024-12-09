from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from service.auth import AuthService
from datetime import timedelta


router = Blueprint("router", __name__)

@router.route('/login', methods=['POST'])
def login():
    body = request.json
    result = AuthService.login_user(body)

    # Generate JWT access token (valid selama 15 menit)
    access_token = create_access_token(identity=result.get("data")[0], expires_delta=timedelta(minutes=15))
    access_token["data"] = {"access_token": access_token}

    return jsonify(result), result["status_code"]

@router.route('/register', methods=['POST'])
def register():
    body = request.json

    result = AuthService.register_user(body)
    return jsonify(result), result["status_code"]

@router.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Optional: Add logic for token blacklisting if needed
    return jsonify({"message": "Logout successful"})

@router.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access_token})

@router.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    mdw = get_jwt_identity()
    user_info = AuthService.get_user_info(mdw)
    return jsonify(user_info)
