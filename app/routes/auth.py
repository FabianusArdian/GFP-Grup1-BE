from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from ..utils.security import token_required
from ..services.user_service import generate_user_id
from ..models.user import User
from ..utils.auth import generate_token
from .. import db
import uuid

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - email
            - password
            - role
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: Password123
            role:
              type: string
              enum: [consumer, seller]
              example: consumer
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input or email already exists
    """
    data = request.get_json()

    # Validasi input
    required_fields = ['name', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400

    # Cek apakah email sudah terdaftar
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    # Buat ID baru untuk user
    user_id = generate_user_id()

    # Buat user baru
    user = User(
        id=user_id,  # Gunakan ID yang dihasilkan
        name=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data['role']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Registration successful',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - email
            - password
            - role
          properties:
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: Password123
            role:
              type: string
              enum: [consumer, seller]
              example: consumer
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json()

    # Validasi input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400

    # Cari user berdasarkan email
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    # Verifikasi password
    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate token
    token = generate_token(user.id)

    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 200

@bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """
    Logout user
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Logout successful
    """
    try:
        # Get response object
        response = jsonify({'message': 'Logout successful'})
        
        # Unset JWT cookies
        unset_jwt_cookies(response)
        
        # Return success response
        return response, 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
