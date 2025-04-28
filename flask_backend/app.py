from flask import Flask, render_template
from models import db
from admin_routes import admin_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(admin_bp)

    # 👉 Voeg HIER je frontend route toe (na de blueprints)
    @app.route('/admin/dashboard')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

