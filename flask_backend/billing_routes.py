# flask_backend/billing_routes.py

from flask import Blueprint, redirect, url_for, session, request
import stripe
from models import db, User
import os
from dotenv import load_dotenv

load_dotenv()

billing_bp = Blueprint('billing', __name__)

# Stripe instellen
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@billing_bp.route('/subscribe')
def subscribe():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': os.getenv('STRIPE_PRICE_ID'),
            'quantity': 1,
        }],
        mode='subscription',
        success_url=url_for('billing.success', _external=True),
        cancel_url=url_for('billing.cancel', _external=True),
        metadata={
            "user_id": user_id
        }
    )
    return redirect(checkout_session.url)

@billing_bp.route('/success')
def success():
    return "Betaling gelukt! Je account wordt nu geüpdatet."

@billing_bp.route('/cancel')
def cancel():
    return "Betaling geannuleerd. Probeer opnieuw."

@billing_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        print(f'⚠️  Webhook fout: {e}')
        return '', 400

    if event['type'] == 'checkout.session.completed':
        session_obj = event['data']['object']
        user_id = session_obj['metadata']['user_id']

        # Gebruiker updaten naar subscriber
        user = User.query.get(user_id)
        if user:
            user.subscription_status = 'subscriber'
            db.session.commit()

    return '', 200
