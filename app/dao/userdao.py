from app.models.user import User

class UserDao:

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)