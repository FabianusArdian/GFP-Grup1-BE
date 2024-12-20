from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models.order import Order

order_routes = Blueprint('orders', __name__)

@order_routes.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    try:
        current_user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=current_user_id).all()
        
        return jsonify([{
            'id': order.id,
            'status': order.status,
            'total_amount': float(order.total_amount),
            'created_at': order.created_at.isoformat(),
            'items': [{
                'id': item.id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price': float(item.price_at_time)
            } for item in order.items]
        } for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
