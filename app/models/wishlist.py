from .. import db
from datetime import datetime

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('wishlist_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('wishlist_items', lazy=True))
