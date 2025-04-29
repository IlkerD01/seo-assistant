# flask_backend/auth_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_backend.models import db, User, InviteCode
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# --- REGISTREREN ROUTE --- #
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        invite_code_input = request.form['invite_code']

        # Controleer invite code
        invite = InviteCode.query.filter_by(code=invite_code_input, used=False).first()
        if not invite:
            error = "Invalid or already used invite code."
            return render_template('register.html', error=error)

        # Check of gebruiker al bestaat
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error = "An account with this email already exists."
            return render_template('register.html', error=error)

        # Maak nieuwe gebruiker aan
        hashed_password = generate_password_hash(password)
        new_user = User(
            email=email,
            password=hashed_password,
            trial_active=True,
            trial_days_left=7,  # Bijv. 7 dagen trial
            trial_searches_left=3,
            subscription_status='trial',
            last_login=datetime.utcnow(),
            searches_done=0
        )
        db.session.add(new_user)
        db.session.commit()

        # Markeer invite code als gebruikt
        invite.used = True
        invite.used_by = new_user.id
        db.session.commit()

        session['user_email'] = new_user.email
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('subscription.account'))

    return render_template('register.html', error=error)

# --- LOGIN ROUTE --- #
@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_email'] = user.email
        session['admin_logged_in'] = True  # ✅ Belangrijk!
        flash('Login successful.', 'success')
        return redirect(url_for('admin.admin_dashboard'))  # ✅ Correct pad

        else:
            error = "Incorrect email or password."

    return render_template('admin_login.html', error=error)

# --- LOGOUT ROUTE --- #
@auth_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)  # ✅ Zorg dat admin sessie verdwijnt
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
