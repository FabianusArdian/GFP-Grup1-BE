from flask_migrate import Migrate
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

# This file will be used with Flask-Migrate commands:
# flask db init
# flask db migrate
# flask db upgrade