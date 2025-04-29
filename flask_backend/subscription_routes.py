# subscription_routes.py

from flask import Blueprint, render_template, session, redirect, url_for
from flask_backend.models import User
from flask import current_app as app
from flask import request
import os

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscribe')
def subscribe():
    return render_template('subscribe.html', stripe_public_key=os.getenv('NEXT_PUBLIC_STRIPE_PUBLIC_KEY'))

@subscription_bp.route('/account')
def account():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=user_email).first()

    if not user:
        return "User not found.", 404

    return render_template('account.html', user=user)
