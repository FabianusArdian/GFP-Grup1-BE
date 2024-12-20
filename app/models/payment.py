from datetime import datetime
from .. import db

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    type = db.Column(db.String(50), nullable=False)  # credit_card, debit_card, etc.
    last_four = db.Column(db.String(4))  # Last 4 digits for cards
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Card-specific fields
    card_brand = db.Column(db.String(20))  # visa, mastercard, etc.
    expiry_month = db.Column(db.String(2))
    expiry_year = db.Column(db.String(2))
    cardholder_name = db.Column(db.String(100))

    # Relationships
    user = db.relationship('User', backref=db.backref('payment_methods', lazy=True))

    def __init__(self, **kwargs):
        super(PaymentMethod, self).__init__(**kwargs)
        if self.is_default:
            # Set all other payment methods of this user to non-default
            PaymentMethod.query.filter_by(
                user_id=self.user_id, 
                is_default=True
            ).update({'is_default': False})
            
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'last_four': self.last_four,
            'is_default': self.is_default,
            'card_brand': self.card_brand,
            'expiry_month': self.expiry_month,
            'expiry_year': self.expiry_year,
            'cardholder_name': self.cardholder_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }