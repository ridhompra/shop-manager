from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from service import auth


router = Blueprint("router", __name__)

@router.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    return jsonify(auth.login_user(email, password))

@router.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    return jsonify(auth.get_user_info())
