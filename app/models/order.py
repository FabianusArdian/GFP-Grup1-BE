from datetime import datetime
from .. import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    status = db.Column(db.Enum('pending', 'processing', 'shipped', 'delivered', 'cancelled'))
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_address_id = db.Column(db.String(36), db.ForeignKey('addresses.id'))
    payment_method = db.Column(db.String(50))

    items = db.relationship('OrderItem', backref='order', lazy=True)
    
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.String(36), primary_key=True)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Numeric(12,2), nullable=False)