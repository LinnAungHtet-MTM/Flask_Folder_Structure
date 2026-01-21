from app.extension import db
from app.models.password_reset import PasswordReset

class PasswordResetDao:

    @staticmethod
    def create(email: str, token: str):
        record = PasswordReset(email=email, token=token)
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def find_valid(email: str, token_hash: str):
        return PasswordReset.query.filter_by(
            email=email,
            token=token_hash,
            deleted_at=None
        ).first()

    @staticmethod
    def find_by_token(token: str):
        return PasswordReset.query.filter_by(token=token, deleted_at=None).first()

    @staticmethod
    def delete_by_token(token: str):
        record = PasswordResetDao.find_by_token(token)
        if record:
            record.deleted_at = datetime.utcnow()
            db.session.commit()
