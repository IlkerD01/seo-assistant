from flask import Flask, render_template, request, redirect, url_for, session
from models import db
from admin_routes import admin_bp

def create_app():
    app = Flask(__name__)

    # Belangrijk: SECRET_KEY voor sessies!
    app.config['SECRET_KEY'] = 'jouw-supergeheime-sleutel-zet-hier-iets-sterk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(admin_bp)

    from auth_routes import auth_bp
    app.register_blueprint(auth_bp)


    # --- Admin login routes --- #
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        error = None
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            if email == "admin@jouwsite.com" and password == "sterkwachtwoord":
                session['admin_logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                error = 'Foutieve login gegevens.'
        return render_template('admin_login.html', error=error)

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        return redirect(url_for('admin_login'))

    # --- Admin frontend pagina's --- #
    @app.route('/admin/dashboard')
    def admin_dashboard():
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return render_template('dashboard.html')

    @app.route('/admin/stats')
    def admin_stats():
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return render_template('stats.html')
    @app.route('/admin/users')
    def admin_users():
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return render_template('users.html')

    return app

# Server starten
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

