# create_admin.py

from flask_backend import app
from flask_backend.models import db, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin(email, password):
    flask_app = app.create_app()
    with flask_app.app_context():
        email = email.strip().lower()  # verwijder spaties en hoofdletters
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            print(f"⚠️ Admin met e-mail '{email}' bestaat al.")
        else:
            hashed_password = generate_password_hash(password)
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
            print(f"✅ Admin '{email}' succesvol aangemaakt!")

# === Vul hier je admin gegevens in ===
if __name__ == "__main__":
    create_admin("idem.85@hotmail.com", "0495")  # 👈 pas dit aan naar jouw e-mailadres en wachtwoord

