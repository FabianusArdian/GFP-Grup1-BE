from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models.user import User

profile_routes = Blueprint('profile', __name__)

@profile_routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'phone': user.phone,
            'created_at': user.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
