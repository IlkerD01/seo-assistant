# routes_billing.py

import stripe
import os
from flask import request, jsonify, render_template
from flask_backend.models import db, User
from flask_backend.app import create_app

app = create_app()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# ➔ Route: Maak Stripe Checkout sessie
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

# ➔ Route: Webhook endpoint
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
        session_data = event['data']['object']
        customer_email = session_data.get('customer_email')
        print('✅ Payment completed for:', customer_email)

        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.is_premium = True
            db.session.commit()
            print(f"✅ User {customer_email} upgraded to premium.")
        else:
            print(f"⚠️ User with email {customer_email} not found.")

    return '', 200

# ➔ Route: Succes pagina na betaling
@app.route('/success')
def payment_success():
    return render_template('success.html')
