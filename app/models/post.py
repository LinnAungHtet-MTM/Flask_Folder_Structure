from datetime import datetime
from app.extension import db
from app.models.base import BaseModel
from app.models.user import User

class Post(db.Model, BaseModel):
    __tablename__ = "posts"

    id = db.Column(db.BigInteger, primary_key = True)
    title = db.Column(db.String(255), nullable = False, unique = True)
    description = db.Column(db.Text, nullable = False)
    status = db.Column(db.Integer, nullable = False, default = 1)
    create_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    updated_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    deleted_user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    create_user = db.relationship("User", foreign_keys=[create_user_id], backref="created_posts")
    updated_user = db.relationship("User", foreign_keys=[updated_user_id], backref="updated_posts")
    deleted_user = db.relationship("User", foreign_keys=[deleted_user_id], backref="deleted_posts")


    def __repr__(self):
        return f"<Post {self.title}>"
