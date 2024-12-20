from flask import Blueprint, request, jsonify
from ..services.seller_service import SellerService
from ..utils.security import token_required
from ..models import Seller, Product, ProductImage

bp = Blueprint('sellers', __name__, url_prefix='/api/sellers')
seller_service = SellerService()

@bp.route('', methods=['GET'])
def get_sellers():
    """
    Get all sellers
    ---
    tags:
      - Sellers
    parameters:
      - name: category
        in: query
        type: string
        required: false
      - name: province
        in: query
        type: string
        required: false
      - name: min_rating
        in: query
        type: number
        required: false
      - name: search
        in: query
        type: string
        required: false
    responses:
      200:
        description: List of sellers
        schema:
          type: array
          items:
            $ref: '#/definitions/Seller'
    """
    filters = {
        'category': request.args.get('category'),
        'province': request.args.get('province'),
        'min_rating': request.args.get('min_rating'),
        'search': request.args.get('search')
    }
    sellers = seller_service.get_sellers(filters)
    return jsonify(sellers), 200

@bp.route('/<seller_id>', methods=['GET'])
def get_seller(seller_id):
    """
    Get a specific seller
    ---
    tags:
      - Sellers
    parameters:
      - name: seller_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Seller details
        schema:
          $ref: '#/definitions/Seller'
      404:
        description: Seller not found
    """
    seller = seller_service.get_seller_by_id(seller_id)
    if not seller:
        return jsonify({'error': 'Seller not found'}), 404
    return jsonify(seller), 200

@bp.route('/<seller_id>/products', methods=['GET'])
def get_seller_products(seller_id):
    """
    Get seller's products
    ---
    tags:
      - Sellers
    parameters:
      - name: seller_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: List of seller's products
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
    """
    try:
        # First verify seller exists
        seller = Seller.query.get_or_404(seller_id)
        
        # Build query for seller's products
        query = Product.query.filter_by(seller_id=seller_id)

        # Apply filters if provided
        if request.args.get('minPrice'):
            query = query.filter(Product.price >= float(request.args.get('minPrice')))
            
        if request.args.get('maxPrice'):
            query = query.filter(Product.price <= float(request.args.get('maxPrice')))
            
        if request.args.get('categories'):
            categories = request.args.get('categories').split(',')
            query = query.filter(Product.category.in_(categories))
            
        if request.args.get('types'):
            types = request.args.get('types').split(',')
            query = query.filter(Product.type.in_(types))
            
        if request.args.get('minRating'):
            query = query.filter(Product.rating >= float(request.args.get('minRating')))
            
        if request.args.get('search'):
            search = f"%{request.args.get('search')}%"
            query = query.filter(
                db.or_(
                    Product.name.ilike(search),
                    Product.description.ilike(search)
                )
            )

        # Execute query and format results
        products = query.all()
        return jsonify([format_product(p) for p in products])

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_seller(seller):
    """Format seller object for API response"""
    return {
        'id': seller.id,
        'name': seller.store_name,
        'description': seller.description,
        'image': seller.image_url,
        'location': seller.location,
        'province': seller.province,
        'rating': float(seller.rating) if seller.rating else 0,
        'category': seller.category,
        'joinedDate': seller.joined_date.isoformat() if seller.joined_date else None,
        'totalProducts': len(seller.products),
        'badges': ['Verified'] if seller.rating and seller.rating >= 4.5 else []
    }

def format_product(product):
    """Format product object for API response"""
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price) if product.price else 0,
        'stock': product.stock or 0,
        'category': product.category,
        'type': product.type,
        'rating': float(product.rating) if product.rating else 0,
        'images': [img.image_url for img in product.images],
        'sellerId': product.seller_id,
        'createdAt': product.created_at.isoformat() if product.created_at else None
    }


@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """
    Update seller profile (Seller only)
    ---
    tags:
      - Sellers
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/definitions/SellerProfileInput'
    responses:
      200:
        description: Profile updated successfully
        schema:
          $ref: '#/definitions/Seller'
      403:
        description: Only sellers can update their profile
      400:
        description: Invalid input
    """
    if current_user.role != 'seller':
        return jsonify({'error': 'Only sellers can update their profile'}), 403
        
    data = request.get_json()
    try:
        profile = seller_service.update_seller_profile(current_user.id, data)
        return jsonify(profile), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Add Swagger definitions
"""
definitions:
  Seller:
    type: object
    properties:
      id:
        type: string
      name:
        type: string
      description:
        type: string
      rating:
        type: number
      image:
        type: string
      location:
        type: string
      province:
        type: string
      category:
        type: string
      joinedDate:
        type: string
        format: date-time
      totalProducts:
        type: integer
      badges:
        type: array
        items:
          type: string
  
  SellerProfileInput:
    type: object
    properties:
      store_name:
        type: string
        example: "Green Valley Farm"
      description:
        type: string
        example: "Fresh organic produce from local farmers"
      location:
        type: string
        example: "Jakarta"
      province:
        type: string
        example: "DKI Jakarta"
      category:
        type: string
        example: "Farmers"
      image_url:
        type: string
        example: "https://example.com/image.jpg"
"""
