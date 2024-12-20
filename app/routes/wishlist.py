from flask import Blueprint, jsonify
from ..services.wishlist_service import WishlistService
from ..utils.security import token_required

bp = Blueprint('wishlist', __name__, url_prefix='/api/wishlist')
wishlist_service = WishlistService()

@bp.route('', methods=['GET'])
@token_required
def get_wishlist(current_user):
    """Get user's wishlist"""
    items = wishlist_service.get_user_wishlist(current_user.id)
    return jsonify(items), 200

@bp.route('/<product_id>', methods=['POST'])
@token_required
def add_to_wishlist(current_user, product_id):
    """Add product to wishlist"""
    if current_user.role != 'consumer':
        return jsonify({'error': 'Only consumers can add to wishlist'}), 403
    item = wishlist_service.add_to_wishlist(current_user.id, product_id)
    return jsonify(item), 201

@bp.route('/<product_id>', methods=['DELETE'])
@token_required
def remove_from_wishlist(current_user, product_id):
    """Remove product from wishlist"""
    wishlist_service.remove_from_wishlist(current_user.id, product_id)
    return jsonify({'message': 'Item removed from wishlist'}), 200
