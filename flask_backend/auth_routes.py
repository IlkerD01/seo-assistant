# flask_backend/auth_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User, InviteCode
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # (optioneel, kun je skippen)
        invite_code = request.form['invite_code']

        # Invite check
        invite = InviteCode.query.filter_by(code=invite_code, used=False).first()
        if not invite:
            flash('Ongeldige of gebruikte invite code.', 'danger')
            return redirect(url_for('auth.register'))

        # Maak gebruiker aan
        new_user = User(
            email=email,
            trial_active=True,
            trial_days_left=7,  # Bijvoorbeeld 7 dagen gratis trial
            trial_searches_left=3,  # 3 gratis zoekopdrachten
            subscription_status='trial',
            last_login=datetime.utcnow(),
            searches_done=0
        )
        db.session.add(new_user)
        db.session.commit()

        # Markeer invite als gebruikt
        invite.used = True
        invite.used_by = new_user.id
        db.session.commit()

        flash('Registratie gelukt. Log nu in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('admin_dashboard'))  # Of een gebruiker dashboard later

        flash('Gebruiker niet gevonden.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
