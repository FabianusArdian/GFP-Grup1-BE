from datetime import datetime
from .. import db

class Seller(db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    store_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    location = db.Column(db.String(100))
    province = db.Column(db.String(50))
    rating = db.Column(db.Numeric(3, 2), default=0)
    category = db.Column(db.String(50))
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='seller', lazy=True)