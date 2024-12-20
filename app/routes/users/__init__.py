from flask import Blueprint
from .profile import profile_routes
from .addresses import address_routes
from .orders import order_routes
from .payments import payment_routes

bp = Blueprint('users', __name__, url_prefix='/api/users')

# Register sub-blueprints
bp.register_blueprint(profile_routes)
bp.register_blueprint(address_routes)
bp.register_blueprint(order_routes)
bp.register_blueprint(payment_routes)
