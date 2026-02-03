from app.extension import db
from datetime import datetime

class PasswordReset(db.Model):
    __tablename__ = "password_resets"

    id = db.Column(db.BigInteger, primary_key = True)
    email = db.Column(db.String(255), nullable = False)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
