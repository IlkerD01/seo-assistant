from flask import Blueprint, jsonify, request, send_file
from models import db, User, SearchLog
from datetime import datetime, timedelta
import csv
import io

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
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

@admin_bp.route('/users/<int:user_id>/searches', methods=['GET'])
def get_user_searches(user_id):
    searches = SearchLog.query.filter_by(user_id=user_id).all()
    search_list = []
    for search in searches:
        search_list.append({
            'query_text': search.query_text,
            'timestamp': search.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(search_list)

@admin_bp.route('/export-searches', methods=['GET'])
def export_searches():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Email', 'Zoekopdracht', 'Datum'])

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

@admin_bp.route('/cleanup-old-searches', methods=['POST'])
def cleanup_old_searches():
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    old_searches = SearchLog.query.filter(SearchLog.timestamp < ninety_days_ago).all()
    for search in old_searches:
        db.session.delete(search)
    db.session.commit()
    return jsonify({'message': f'{len(old_searches)} oude zoekopdrachten verwijderd'})


@admin_bp.route('/api/admin/export-searches', methods=['GET'])
def export_searches():
    output = io.StringIO()
    writer = csv.writer(output)
    
    # CSV Header
    writer.writerow(['Gebruiker Email', 'Zoekopdracht', 'Tijdstip'])

    users = User.query.all()
    for user in users:
        for search in user.searches:
            writer.writerow([user.email, search.query_text, search.timestamp])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"zoekopdrachten_export_{datetime.date.today()}.csv"
    )

