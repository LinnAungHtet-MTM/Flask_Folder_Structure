from app.dao.userdao import UserDao

class UserService:

    @staticmethod
    def get_login_user(user_id):
        return UserDao.find_by_id(user_id)