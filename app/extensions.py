
from flask_jwt_extended import JWTManager
from datetime import timedelta

jwt = JWTManager()

def init_extensions(app):
    """Initialize Flask extensions"""
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    jwt.init_app(app)
