from flask_cors import CORS

def configure_cors(app):
    """Configure CORS settings for the application"""
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",  # Next.js development server
                "http://127.0.0.1:3000",
                # Add production domains here
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Range", "X-Total-Count"],
            "supports_credentials": True,
            "max_age": 600,  # Cache preflight requests for 10 minutes
        }
    })
