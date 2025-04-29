from flask_backend.models import db, User
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_backend import app  # Zorg dat dit je create_app-functie aanroept

# Start Flask app context
flask_app = app.create_app()
with flask_app.app_context():
    email = "idem.85@hotmail.com   "
    password = "0495"
    hashed_password = generate_password_hash(password)

    # Check of admin al bestaat
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print("Admin bestaat al.")
    else:
        new_admin = User(
            email=email,
            password=hashed_password,
            trial_active=False,
            trial_days_left=0,
            trial_searches_left=0,
            subscription_status="admin",
            last_login=datetime.utcnow(),
            searches_done=0
        )
        db.session.add(new_admin)
        db.session.commit()
        print("✅ Admin succesvol toegevoegd.")
