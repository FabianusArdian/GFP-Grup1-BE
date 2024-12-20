from flask import Blueprint, render_template
from flasgger import Swagger
from .swagger_docs import order_routes

bp = Blueprint('api_docs', __name__)

# Swagger template configuration
template = {
    "swagger": "2.0",
    "info": {
        "title": "Local Food Market API",
        "description": "API documentation for Local Food Market platform",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@localfoodmarket.com"
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
        }
    },
    "security": [{"Bearer": []}],
    "paths": order_routes,
    "definitions": {
        "Order": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "example": "o1"},
                "user_id": {"type": "string", "example": "u1"},
                "status": {
                    "type": "string",
                    "enum": ["pending", "processing", "shipped", "delivered", "cancelled"]
                },
                "total_amount": {"type": "number", "format": "float"},
                "created_at": {"type": "string", "format": "date-time"},
                "shipping_address_id": {"type": "string"},
                "payment_method": {"type": "string"}
            }
        }
    }
}

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

def init_app(app):
    # Initialize Swagger
    Swagger(app, template=template, config=swagger_config)
    
    # Register blueprint
    app.register_blueprint(bp)

    # API Documentation route
    @bp.route('/')
    @bp.route('/api')
    def api_docs():
        return render_template('api_docs.html')
