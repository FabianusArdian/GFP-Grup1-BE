from typing import Dict, Any, List
import uuid
from ..models.order import Order, OrderItem
from ..models.product import Product
from .. import db

class OrderService:
    def create_order(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Calculate total and validate stock
        total_amount = 0
        order_items = []
        
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product:
                raise ValueError(f"Product {item['product_id']} not found")
                
            if product.stock < item['quantity']:
                raise ValueError(f"Insufficient stock for {product.name}")
                
            total_amount += float(product.price) * item['quantity']
            order_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': float(product.price)
            })
            
        # Create order
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            status='pending',
            total_amount=total_amount,
            shipping_address_id=data['shipping_address_id'],
            payment_method=data['payment_method']
        )
        
        # Create order items and update stock
        for item in order_items:
            order_item = OrderItem(
                id=str(uuid.uuid4()),
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price_at_time=item['price']
            )
            order.items.append(order_item)
            
            # Update product stock
            item['product'].stock -= item['quantity']
            
        db.session.add(order)
        db.session.commit()
        
        return self._format_order(order)
        
    def get_user_orders(self, user_id: str) -> List[Dict[str, Any]]:
        orders = Order.query.filter_by(user_id=user_id).all()
        return [self._format_order(o) for o in orders]
        
    def _format_order(self, order: Order) -> Dict[str, Any]:
        return {
            'id': order.id,
            'status': order.status,
            'total_amount': float(order.total_amount),
            'created_at': order.created_at.isoformat(),
            'items': [{
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price': float(item.price_at_time)
            } for item in order.items],
            'shipping_address_id': order.shipping_address_id,
            'payment_method': order.payment_method
        }
