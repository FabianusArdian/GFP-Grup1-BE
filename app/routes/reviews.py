from flask import Blueprint, request, jsonify
from ..services.review_service import ReviewService
from ..utils.security import token_required

bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')
review_service = ReviewService()

@bp.route('/products/<product_id>', methods=['POST'])
@token_required
def create_review(current_user, product_id):
    """Create product review (must have ordered the product)"""
    if current_user.role != 'consumer':
        return jsonify({'error': 'Only consumers can write reviews'}), 403
    data = request.get_json()
    review = review_service.create_review(
        user_id=current_user.id,
        product_id=product_id,
        rating=data.get('rating'),
        comment=data.get('comment')
    )
    return jsonify(review), 201

@bp.route('/products/<product_id>', methods=['GET'])
def get_product_reviews(product_id):
    """Get product reviews"""
    reviews = review_service.get_product_reviews(product_id)
    return jsonify(reviews), 200

@bp.route('/<review_id>', methods=['PUT', 'DELETE'])
@token_required
def manage_review(current_user, review_id):
    """Update or delete review (owner only)"""
    review = review_service.get_review_by_id(review_id)
    if not review or review.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if request.method == 'PUT':
        data = request.get_json()
        updated = review_service.update_review(review_id, data)
        return jsonify(updated), 200
    
    review_service.delete_review(review_id)
    return jsonify({'message': 'Review deleted'}), 200
