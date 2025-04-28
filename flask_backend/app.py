# app.py

from flask import Flask
from models import db
from admin_routes import admin_bp
from billing_routes import billing_bp
from auth_routes import auth_bp

def create_app():
    app = Flask(__name__)

    # Belangrijk: Geheime sleutels en database configuratie
    app.config['SECRET_KEY'] = 'jouw-supergeheime-sleutel-zet-hier-iets-sterk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(auth_bp)

    return app

# Server starten
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)


