from flask import Flask, render_template, request, redirect, url_for, session
from models import db
from admin_routes import admin_bp
from billing_routes import billing_bp
import stripe
import os
from flask import Flask, request, jsonify, redirect, abort

def create_app():
    app = Flask(__name__)

    # Belangrijk: SECRET_KEY voor sessies!
    app.config['SECRET_KEY'] = 'jouw-supergeheime-sleutel-zet-hier-iets-sterk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(billing_bp)

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

    @app.route('/create-checkout-session', methods=['POST'])
    def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': os.getenv('STRIPE_PRICE_ID'),
                'quantity': 1,
            }],
            success_url=os.getenv('SUCCESS_URL') + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=os.getenv('CANCEL_URL'),
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 400

    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    @app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print('⚠️ Invalid payload', e)
        return '', 400
    except stripe.error.SignatureVerificationError as e:
        print('⚠️ Invalid signature', e)
        return '', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')
        print('✅ Payment completed for:', customer_email)

        # ACTIVEER PREMIUM ACCOUNT
        from models import User  # Zorg dat je User model hebt
        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.is_premium = True
            db.session.commit()
            print(f"✅ User {customer_email} upgraded to premium.")
        else:
            print(f"⚠️ User with email {customer_email} not found.")

    return '', 200

    @app.route('/success')
    def payment_success():
    return render_template('success.html')


# Server starten
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

