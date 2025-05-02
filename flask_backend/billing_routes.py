# flask_backend/billing_routes.py

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import os
import stripe
from flask_backend.models import db, User

billing_bp = Blueprint('billing', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@billing_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # User must be logged in

    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('auth.login'))

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            customer_email=user.email,
            line_items=[{
                'price': os.getenv('STRIPE_PRICE_ID'),
                'quantity': 1,
            }],
            success_url=os.getenv('SUCCESS_URL') + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=os.getenv('CANCEL_URL'),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@billing_bp.route('/success')
def payment_success():
    return render_template('success.html')

@billing_bp.route('/cancel')
def payment_cancel():
    return render_template('cancel.html')

@billing_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        print('⚠️ Invalid payload', e)
        return '', 400
    except stripe.error.SignatureVerificationError as e:
        print('⚠️ Invalid signature', e)
        return '', 400

    if event['type'] == 'checkout.session.completed':
        session_obj = event['data']['object']
        customer_email = session_obj.get('customer_email')

        if customer_email:
            user = User.query.filter_by(email=customer_email).first()
            if user:
                user.subscription_status = 'premium'
                user.is_premium = True
                db.session.commit()
                print(f'✅ {customer_email} upgraded to premium.')
            else:
                print(f'⚠️ User {customer_email} not found.')

    return '', 200
