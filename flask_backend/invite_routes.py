# flask_backend/invite_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, InviteCode
import random
import string

invite_bp = Blueprint('invite', __name__)

def generate_invite_code(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@invite_bp.route('/admin/invites')
def admin_invites():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    invites = InviteCode.query.order_by(InviteCode.id.desc()).all()  # Laatste invites bovenaan
    return render_template('invite_admin.html', invites=invites)

@invite_bp.route('/admin/invites/create', methods=['POST'])
def create_invite():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    new_code = generate_invite_code()
    invite = InviteCode(code=new_code)
    db.session.add(invite)
    db.session.commit()

    flash('✅ Invite code successfully created.', 'success')
    return redirect(url_for('invite.admin_invites'))

@invite_bp.route('/admin/invites/delete/<int:invite_id>', methods=['POST'])
def delete_invite(invite_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    invite = InviteCode.query.get_or_404(invite_id)
    db.session.delete(invite)
    db.session.commit()

    flash('❌ Invite code deleted.', 'danger')
    return redirect(url_for('invite.admin_invites'))
