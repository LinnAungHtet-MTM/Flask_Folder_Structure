from app.extension import db
from app.models.user import User
from datetime import datetime, timedelta, time


class UserDao:

    @staticmethod
    def find_by_email(email):
        return User.query.filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()

    @staticmethod
    def find_by_email_or_name(email, name):
        return User.query.filter(
            (User.email == email) | (User.name == name),
            # User.deleted_at.is_(None)
        ).first()

    @staticmethod
    def find_by_email_or_name_exclude_current_user(email, name, user_id):
        return User.query.filter(
            (User.email == email) | (User.name == name),
            User.id != user_id,
            User.deleted_at.is_(None)
        ).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.filter(
            User.id == user_id,
            User.deleted_at.is_(None)
        ).first()

    @staticmethod
    def get_all_users(page, per_page):
        query = User.query.filter(User.deleted_at.is_(None))
        return query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def find_by_ids(user_ids: list[int]):
        return User.query.filter(
            User.id.in_(user_ids),
            User.deleted_at.is_(None)
        ).all()

    @staticmethod
    def update_lock_status(users: list[User], lock_flg: int):
        for user in users:
            user.lock_flg = lock_flg

    @staticmethod
    def create_user(**kwargs):
        user = User(**kwargs)
        db.session.add(user)
        return user

    @staticmethod
    def update_user(user, **kwargs):
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user

    @staticmethod
    def delete_users(users: list[User], deleted_user_id):
        for user in users:
            user.deleted_at = datetime.utcnow()
            user.deleted_user_id = deleted_user_id

    @staticmethod
    def search_users(name=None, email=None, role=None, start_date=None, end_date=None, page=1, per_page=10):
        query = User.query.filter(User.deleted_at.is_(None))

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))

        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))

        if role is not None:
            query = query.filter(User.role == int(role))

        # Date filter logic
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            start = datetime.combine(start.date(), time.min)
            query = query.filter(User.created_at >= start)

        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            end = datetime.combine(end.date(), time.max)
            query = query.filter(User.created_at <= end)

        return query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
