
from flask import Blueprint, request, jsonify
from ..models import Product, ProductImage, Seller
from ..services.product_service import ProductService
from ..utils.security import token_required

bp = Blueprint('products', __name__, url_prefix='/api/products')
product_service = ProductService()

@bp.route('', methods=['GET'])
def get_products():
    """
    Get all products
    ---
    tags:
      - Products
    parameters:
      - name: category
        in: query
        type: string
        required: false
      - name: type
        in: query
        type: string
        required: false
      - name: min_price
        in: query
        type: number
        required: false
      - name: max_price
        in: query
        type: number
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
        description: List of products
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
    """
    try:
        query = Product.query

        # Get featured products (top 3 by rating)
        if request.args.get('featured') == 'true':
            return jsonify([
                format_product(p) for p in 
                Product.query.order_by(Product.rating.desc()).limit(3).all()
            ])

        # Apply other filters
        if request.args.get('category'):
            query = query.filter(Product.category == request.args.get('category'))
            
        if request.args.get('minPrice'):
            query = query.filter(Product.price >= float(request.args.get('minPrice')))
            
        if request.args.get('maxPrice'):
            query = query.filter(Product.price <= float(request.args.get('maxPrice')))
            
        if request.args.get('search'):
            search = f"%{request.args.get('search')}%"
            query = query.filter(
                db.or_(
                    Product.name.ilike(search),
                    Product.description.ilike(search)
                )
            )

        products = query.all()
        return jsonify([format_product(p) for p in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a specific product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Product details
        schema:
          $ref: '#/definitions/Product'
      404:
        description: Product not found
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
            
        return jsonify(format_product(product))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_product(product):
    """Format product object for API response"""
    seller = Seller.query.get(product.seller_id)
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'stock': product.stock,
        'category': product.category,
        'type': product.type,
        'rating': float(product.rating),
        'images': [img.image_url for img in product.images],
        'sellerId': product.seller_id,
        'sellerName': seller.store_name if seller else None,
        'createdAt': product.created_at.isoformat()
    }

@bp.route('', methods=['POST'])
@token_required
def create_product(current_user):
    """
    Create a new product (Seller only)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/ProductInput'
    responses:
      201:
        description: Product created successfully
        schema:
          $ref: '#/definitions/Product'
      403:
        description: Only sellers can create products
        schema:
          type: object
          properties:
            error:
              type: string
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if current_user.role != 'seller':
        return jsonify({'error': 'Only sellers can create products'}), 403
        
    data = request.get_json()
    try:
        product = product_service.create_product(current_user.id, data)
        return jsonify(product), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    """
    Update a product (Seller only)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/ProductInput'
    responses:
      200:
        description: Product updated successfully
        schema:
          $ref: '#/definitions/Product'
      403:
        description: Only sellers can update products
      404:
        description: Product not found
      400:
        description: Invalid input
    """
    if current_user.role != 'seller':
        return jsonify({'error': 'Only sellers can update products'}), 403
        
    data = request.get_json()
    try:
        product = product_service.update_product(current_user.id, product_id, data)
        return jsonify(product), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

"""
definitions:
  ProductInput:
    type: object
    required:
      - name
      - description
      - price
      - stock
      - category
      - type
    properties:
      name:
        type: string
        example: "Organic Vegetable Box"
      description:
        type: string
        example: "Fresh organic vegetables from local farms."
      price:
        type: number
        example: 150000
      stock:
        type: integer
        example: 50
      category:
        type: string
        example: "Fresh Produce"
      type:
        type: string
        enum: [standard, premium]
        example: "premium"
      images:
        type: array
        items:
          type: string
          example: "https://example.com/image1.jpg"

  Product:
    type: object
    properties:
      id:
        type: string
        example: "product-uuid"
      name:
        type: string
        example: "Organic Vegetable Box"
      description:
        type: string
        example: "Fresh organic vegetables from local farms."
      price:
        type: number
        example: 150000
      stock:
        type: integer
        example: 50
      category:
        type: string
        example: "Fresh Produce"
      type:
        type: string
        example: "premium"
      rating:
        type: number
        example: 4.5
      images:
        type: array
        items:
          type: string
          example: "https://example.com/image1.jpg"
      seller_id:
        type: string
        example: "seller-uuid"
      created_at:
        type: string
        format: date-time
        example: "2024-06-01T12:00:00"
"""
