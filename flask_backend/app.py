from flask import Flask, redirect
from flask_backend.models import db
from flask_backend.admin_routes import admin_bp
from flask_backend.billing_routes import billing_bp
from flask_backend.auth_routes import auth_bp
from flask_backend.subscription_routes import subscription_bp

def create_app():
    app = Flask(__name__)

    # Configuratie
    app.config['SECRET_KEY'] = 'jouw-supergeheime-sleutel-zet-hier-iets-sterk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ✅ Zet hier de route binnen create_app
    @app.route('/')
    def index():
        return redirect('/auth/admin-login')

    # Register blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(subscription_bp)

    return app  # ✅ juiste plaats

# Server starten
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
