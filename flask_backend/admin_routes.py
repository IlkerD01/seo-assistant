# flask_backend/admin_routes.py

from flask import Blueprint, render_template, jsonify, request, send_file, session, redirect, url_for, flash
from flask_backend.models import User, SearchLog
from datetime import datetime, timedelta
import csv
import io
import smtplib
from email.mime.text import MIMEText
import random
import string
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Dashboard pagina
@admin_bp.route('/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('auth.login'))
    return render_template('admin_dashboard.html')

# API: Alle gebruikers ophalen
@admin_bp.route('/users', methods=['GET'])
def get_users():
    users = none.query.with_entities(
        User.id,
        User.email,
        User.trial_active,
        User.trial_days_left,
        User.trial_searches_left,
        User.searches_done,
        User.last_login,
        User.subscription_status
    ).all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'trial_active': user.trial_active,
            'trial_days_left': user.trial_days_left,
            'trial_searches_left': user.trial_searches_left,
            'searches_done': user.searches_done,
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None,
            'subscription_status': user.subscription_status
        })
    return jsonify(user_list)


# API: Nieuwe gebruiker toevoegen
@admin_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        email=data['email'],
        trial_active=data['trial_active'],
        trial_days_left=data['trial_days_left'],
        trial_searches_left=data['trial_searches_left'],
        searches_done=0,
        last_login=datetime.utcnow(),
        subscription_status=data['subscription_status']
    )
    db.session.add(new_user)
    db.session.commit()
    send_email_notification(new_user.email)
    return jsonify({'message': 'User added successfully'}), 201

# API: Gebruiker verwijderen
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

# API: Dashboard statistieken ophalen
@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    total_users = db.session.query(func.count(User.id)).scalar()
    total_searches = db.session.query(func.count(SearchLog.id)).scalar()
    return jsonify({
        'total_users': total_users,
        'total_searches': total_searches
    })

# API: Exporteer zoekopdrachten
@admin_bp.route('/export-searches', methods=['GET'])
def export_searches():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Email', 'Query', 'Timestamp'])

    logs = SearchLog.query.join(User).add_columns(User.email, SearchLog.query_text, SearchLog.timestamp).all()
    for log in logs:
        writer.writerow([log.email, log.query_text, log.timestamp.strftime('%Y-%m-%d %H:%M:%S')])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='search_logs.csv'
    )

# E-mail versturen
def send_email_notification(email):
    try:
        sender = 'jouwmail@gmail.com'
        receiver = 'jouwmail@gmail.com'
        password = 'jouw-apparaatwachtwoord'

        msg = MIMEText(f'New user registered: {email}')
        msg['Subject'] = 'New User Notification'
        msg['From'] = sender
        msg['To'] = receiver

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Email sending error: {e}")

# Invite codes
@admin_bp.route('/invite-codes', methods=['GET', 'POST'])
def invite_codes():
    if not session.get('admin_logged_in'):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        new_code = InviteCode(code=code)
        db.session.add(new_code)
        db.session.commit()
        flash(f'New invite code created: {code}', 'success')
        return redirect(url_for('admin.invite_codes'))

    invites = InviteCode.query.all()
    return render_template('invite_codes.html', invites=invites)

# Statistieken: nieuwe gebruikers per week
@admin_bp.route('/stats/weekly-users', methods=['GET'])
def weekly_users():
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    users = User.query.filter(User.last_login >= one_month_ago).all()

    weekly_data = {}
    for user in users:
        week = user.last_login.strftime('%Y-W%U')
        weekly_data[week] = weekly_data.get(week, 0) + 1

    sorted_data = sorted(weekly_data.items())
    labels = [item[0] for item in sorted_data]
    counts = [item[1] for item in sorted_data]

    return jsonify({"labels": labels, "counts": counts})

# Statistieken: totaal users / searches
@admin_bp.route('/stats-data')
def admin_stats_data():
    total_users = User.query.count()
    premium_users = User.query.filter_by(subscription_status='premium').count()
    trial_users = User.query.filter_by(subscription_status='trial').count()
    total_searches = db.session.query(func.count(SearchLog.id)).scalar()

    return jsonify({
        'total_users': total_users,
        'premium_users': premium_users,
        'trial_users': trial_users,
        'total_searches': total_searches
    })

# New Users Per Week (extra)
@admin_bp.route('/new-users-per-week', methods=['GET'])
def new_users_per_week():
    today = datetime.utcnow()
    weeks = []
    counts = []

    for i in range(5, -1, -1):
        start_date = today - timedelta(weeks=i+1)
        end_date = today - timedelta(weeks=i)
        week_label = f"Week {start_date.isocalendar()[1]}"

        count = User.query.filter(User.last_login >= start_date, User.last_login < end_date).count()

        weeks.append(week_label)
        counts.append(count)

    return jsonify({'weeks': weeks, 'counts': counts})



