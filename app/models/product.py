from datetime import datetime
from .. import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True)
    seller_id = db.Column(db.String(36), db.ForeignKey('sellers.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    type = db.Column(db.Enum('standard', 'premium'), default='standard')
    rating = db.Column(db.Numeric(3, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('ProductImage', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
class ProductImage(db.Model):
    __tablename__ = 'product_images'
    
    id = db.Column(db.String(36), primary_key=True)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)