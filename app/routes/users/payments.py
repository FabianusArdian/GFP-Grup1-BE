from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models.payment import PaymentMethod

payment_routes = Blueprint('payments', __name__)

@payment_routes.route('/payment-methods', methods=['GET'])
@jwt_required()
def get_payment_methods():
    """Get user's payment methods"""
    try:
        current_user_id = get_jwt_identity()
        payment_methods = PaymentMethod.query.filter_by(user_id=current_user_id).all()
        
        return jsonify([{
            'id': pm.id,
            'type': pm.type,
            'provider': pm.provider,
            'last_four': pm.last_four if hasattr(pm, 'last_four') else None,
            'expiry_date': pm.expiry_date.isoformat() if hasattr(pm, 'expiry_date') else None,
            'is_default': pm.is_default
        } for pm in payment_methods]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
