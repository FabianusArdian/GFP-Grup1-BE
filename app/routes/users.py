
from flask import Blueprint, request, jsonify
from ..services.user_service import UserService
from ..utils.security import token_required
from ..utils.validators import validate_phone

bp = Blueprint('users', __name__, url_prefix='/api/users')
user_service = UserService()

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Get current user's profile
    ---
    tags:
      - User Profile
    security:
      - Bearer: []
    responses:
      200:
        description: User profile details
        schema:
          $ref: '#/definitions/UserProfile'
      400:
        description: Error retrieving profile
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        profile = user_service.get_user_profile(current_user.id)
        return jsonify(profile), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """
    Update current user's profile
    ---
    tags:
      - User Profile
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "John Doe"
            phone:
              type: string
              example: "081234567890"
    responses:
      200:
        description: Profile updated successfully
        schema:
          $ref: '#/definitions/UserProfile'
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    
    if data.get('phone') and not validate_phone(data['phone']):
        return jsonify({'error': 'Invalid phone number format'}), 400
    
    try:
        profile = user_service.update_user_profile(current_user.id, data)
        return jsonify(profile), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/addresses', methods=['GET'])
@token_required
def get_addresses(current_user):
    """
    Get user's shipping addresses
    ---
    tags:
      - User Profile
    security:
      - Bearer: []
    responses:
      200:
        description: List of user's addresses
        schema:
          type: array
          items:
            $ref: '#/definitions/Address'
      400:
        description: Error retrieving addresses
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        addresses = user_service.get_user_addresses(current_user.id)
        return jsonify(addresses), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/addresses', methods=['POST'])
@token_required
def add_address(current_user):
    """
    Add new shipping address
    ---
    tags:
      - User Profile
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/AddressInput'
    responses:
      201:
        description: Address added successfully
        schema:
          $ref: '#/definitions/Address'
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    try:
        address = user_service.add_user_address(current_user.id, data)
        return jsonify(address), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Add Swagger definitions
"""
definitions:
  UserProfile:
    type: object
    properties:
      id:
        type: string
      name:
        type: string
      email:
        type: string
      role:
        type: string
        enum: [consumer, seller]
      phone:
        type: string
      created_at:
        type: string
        format: date-time

  Address:
    type: object
    properties:
      id:
        type: string
      label:
        type: string
        example: "Home"
      name:
        type: string
      phone:
        type: string
      address:
        type: string
      city:
        type: string
      province:
        type: string
      postal_code:
        type: string
      is_default:
        type: boolean

  AddressInput:
    type: object
    required:
      - label
      - name
      - phone
      - address
      - city
      - province
      - postal_code
    properties:
      label:
        type: string
        example: "Home"
      name:
        type: string
        example: "John Doe"
      phone:
        type: string
        example: "081234567890"
      address:
        type: string
        example: "Jl. Sudirman No. 123"
      city:
        type: string
        example: "Jakarta"
      province:
        type: string
        example: "DKI Jakarta"
      postal_code:
        type: string
        example: "12345"
      is_default:
        type: boolean
        example: false
"""
