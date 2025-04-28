# backend/app/__init__.py

from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # DATABASE SETTINGS
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # of PostgreSQL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .admin_routes import admin_bp
    from .stripe_routes import stripe_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(stripe_bp)

    return app
