
from flask import Blueprint, request, jsonify
from ..services.order_service import OrderService
from ..utils.security import token_required

bp = Blueprint('orders', __name__, url_prefix='/api/orders')
order_service = OrderService()

@bp.route('', methods=['GET'])
@token_required
def get_orders(current_user):
    """
    Get user's orders
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    responses:
      200:
        description: List of user's orders
        schema:
          type: array
          items:
            $ref: '#/definitions/Order'
      400:
        description: Error retrieving orders
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        orders = order_service.get_user_orders(current_user.id)
        return jsonify(orders), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('', methods=['POST'])
@token_required
def create_order(current_user):
    """
    Create a new order
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - items
            - shipping_address_id
            - payment_method
          properties:
            items:
              type: array
              items:
                type: object
                required:
                  - product_id
                  - quantity
                properties:
                  product_id:
                    type: string
                    example: "123"
                  quantity:
                    type: integer
                    example: 2
            shipping_address_id:
              type: string
              example: "addr_123"
            payment_method:
              type: string
              example: "credit_card"
    responses:
      201:
        description: Order created successfully
        schema:
          $ref: '#/definitions/Order'
      403:
        description: Only consumers can create orders
        schema:
          type: object
          properties:
            error:
              type: string
      400:
        description: Invalid input or insufficient stock
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if current_user.role != 'consumer':
        return jsonify({'error': 'Only consumers can create orders'}), 403
        
    data = request.get_json()
    try:
        order = order_service.create_order(current_user.id, data)
        return jsonify(order), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<order_id>', methods=['GET'])
@token_required
def get_order(current_user, order_id):
    """
    Get specific order details
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - name: order_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Order details
        schema:
          $ref: '#/definitions/Order'
      403:
        description: Unauthorized access
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Order not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        order = order_service.get_order_by_id(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
            
        # Verify order belongs to user or seller
        if (current_user.role == 'consumer' and order['user_id'] != current_user.id) or \
           (current_user.role == 'seller' and order['seller_id'] != current_user.id):
            return jsonify({'error': 'Unauthorized access'}), 403
            
        return jsonify(order), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<order_id>/status', methods=['PUT'])
@token_required
def update_order_status(current_user, order_id):
    """
    Update order status (Seller only)
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - name: order_id
        in: path
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum: [pending, processing, shipped, delivered, cancelled]
              example: "processing"
            note:
              type: string
              example: "Order is being prepared"
    responses:
      200:
        description: Order status updated successfully
        schema:
          $ref: '#/definitions/Order'
      403:
        description: Only sellers can update order status
        schema:
          type: object
          properties:
            error:
              type: string
      400:
        description: Invalid status or error updating order
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if current_user.role != 'seller':
        return jsonify({'error': 'Only sellers can update order status'}), 403
        
    data = request.get_json()
    try:
        order = order_service.update_order_status(
            order_id=order_id,
            seller_id=current_user.id,
            new_status=data.get('status'),
            note=data.get('note')
        )
        return jsonify(order), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Add Swagger definitions
"""
definitions:
  Order:
    type: object
    properties:
      id:
        type: string
      user_id:
        type: string
      status:
        type: string
        enum: [pending, processing, shipped, delivered, cancelled]
      total_amount:
        type: number
      created_at:
        type: string
        format: date-time
      shipping_address_id:
        type: string
      payment_method:
        type: string
      items:
        type: array
        items:
          type: object
          properties:
            product_id:
              type: string
            quantity:
              type: integer
            price_at_time:
              type: number
      status_history:
        type: array
        items:
          type: object
          properties:
            status:
              type: string
            timestamp:
              type: string
              format: date-time
            note:
              type: string
            updated_by:
              type: string
"""
