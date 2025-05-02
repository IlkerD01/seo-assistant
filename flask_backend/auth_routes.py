from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_backend.models import db, User, InviteCode
from datetime import datetime

auth_bp = Blueprint('auth', __name__)  # 👈 Dit moet eerst komen

# --- TIJDELIJKE ADMIN AANMAAKROUTE --- #
@auth_bp.route('/create-admin-once')
def create_admin_once():
    email = "idem.85@hotmail.com"
    password = "0495"
    email_clean = email.strip().lower()

    existing_user = User.query.filter_by(email=email_clean).first()
    if existing_user:
        return jsonify({"message": f"⚠️ Admin '{email_clean}' bestaat al."})

    hashed = generate_password_hash(password)
    new_admin = User(
        email=email_clean,
        password=hashed,
        trial_active=False,
        trial_days_left=0,
        trial_searches_left=0,
        subscription_status="admin",
        last_login=datetime.utcnow(),
        searches_done=0
    )
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({
        "message": "✅ Admin succesvol aangemaakt!",
        "email": email_clean,
        "wachtwoord": password
    })
