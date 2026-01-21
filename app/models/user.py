from datetime import datetime
from app.extension import db
from app.models.base import BaseModel

class User(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key = True)
    name = db.Column(db.String(255), nullable = False, unique = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255))
    profile_path = db.Column(db.String(255))
    role = db.Column(db.Boolean, nullable = False, default = True)
    dob = db.Column(db.Date)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    lock_flg = db.Column(db.Boolean, nullable = False, default = False)
    lock_count = db.Column(db.Integer, default = 0)
    last_lock_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    create_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    updated_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    deleted_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User {self.name}>"
