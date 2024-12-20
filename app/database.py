
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database and migrations"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they're registered
    from .models import user, address, order, product, seller, payment
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
            raise
