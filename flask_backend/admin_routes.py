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

# API voor admin dashboard statistieken
@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    total_users = User.query.count()
    total_searches = SearchLog.query.count()

    # Simuleer activiteit laatste 7 dagen
    activity = {
        'days': [],
        'counts': []
    }
    today = datetime.utcnow()
    for i in range(7):
        day = today - timedelta(days=i)
        count = SearchLog.query.filter(
            SearchLog.timestamp >= day.replace(hour=0, minute=0, second=0),
            SearchLog.timestamp <= day.replace(hour=23, minute=59, second=59)
        ).count()
        activity['days'].insert(0, day.strftime('%d-%m'))
        activity['counts'].insert(0, count)

    return jsonify({
        'total_users': total_users,
        'total_searches': total_searches,
        'activity': activity
    })

# API voor top 5 actieve gebruikers
@admin_bp.route('/top-users', methods=['GET'])
def get_top_users():
    users = User.query.all()
    user_stats = []

    for user in users:
        user_stats.append({
            'email': user.email,
            'search_count': len(user.searches)
        })

    # Sorteer op zoekopdrachten
    sorted_users = sorted(user_stats, key=lambda x: x['search_count'], reverse=True)[:5]

    return jsonify({
        'users': [u['email'] for u in sorted_users],
        'search_counts': [u['search_count'] for u in sorted_users]
    })



