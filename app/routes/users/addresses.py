from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models.address import Address

address_routes = Blueprint('addresses', __name__)

@address_routes.route('/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    """Get user's addresses"""
    try:
        current_user_id = get_jwt_identity()
        addresses = Address.query.filter_by(user_id=current_user_id).all()
        
        return jsonify([{
            'id': addr.id,
            'label': addr.label,
            'name': addr.name,
            'phone': addr.phone,
            'address': addr.address,
            'city': addr.city,
            'province': addr.province,
            'postal_code': addr.postal_code,
            'is_default': addr.is_default
        } for addr in addresses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
