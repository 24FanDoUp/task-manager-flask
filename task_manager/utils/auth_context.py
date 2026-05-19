from flask import session
from extensions import manager
from database.models import User

def inject_user():
    user_id = session.get("user_id")
    user = None

    if user_id:
        user = manager.db.query(User).filter_by(id=user_id).first()

    return dict(
        is_logged_in = "user_id" in session,
        current_user = user)
