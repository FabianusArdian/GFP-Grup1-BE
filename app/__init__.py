from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from .config import Config
from .config.cors import configure_cors
from .swagger_config import template, swagger_config
import pymysql

# Replace MySQL driver
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Import models
    with app.app_context():
        from .models import User, Address, Order, OrderItem, Product, ProductImage, Seller, WishlistItem
        db.create_all()
    
    configure_cors(app)  # Configure CORS
    Swagger(app, template=template, config=swagger_config)
    
    # Register blueprints
    from .routes import auth, products, sellers, orders, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(sellers.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(users.bp)
    
    # API Documentation route
    @app.route('/')
    @app.route('/api')
    def api_docs():
        return render_template('api_docs.html')
    
    return app
