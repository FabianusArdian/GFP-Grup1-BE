from .. import db

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    label = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    
    def __init__(self, **kwargs):
        super(Address, self).__init__(**kwargs)
        if self.is_default:
            # Set all other addresses of this user to non-default
            Address.query.filter_by(
                user_id=self.user_id, 
                is_default=True
            ).update({'is_default': False})
