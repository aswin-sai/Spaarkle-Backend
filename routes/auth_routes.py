from flask import Blueprint, request, jsonify
from models import AdminUser
from extensions import db
from utils.auth import verify_password, create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = AdminUser.query.filter_by(email=data.get('email')).first()
    if user and verify_password(data.get('password'), user.hashed_password):
        token = create_access_token(identity=user.id)
        return jsonify({'access_token': token})
    return jsonify({'error': 'Invalid credentials'}), 401
