from app.dao.userdao import UserDao
from app.exceptions.business_exception import BusinessException
from app.utils.file_upload import allowed_file
from werkzeug.security import generate_password_hash
import cloudinary.uploader


class UserService:

    @staticmethod
    def get_user_by_id(user_id):
        user = UserDao.find_by_id(user_id)

        if not user:
            return {
                "success": False,
                "field": "user_id",
                "message": "User not found"
            }

        created_user = None
        updated_user = None

        if user.create_user_id:
            created_user = UserDao.find_by_id(user.create_user_id)
            if created_user:
                created_user = "User" if created_user.role else "Admin"
        if user.updated_user_id:
            updated_user = UserDao.find_by_id(user.updated_user_id)
            if updated_user:
                updated_user = "User" if updated_user.role else "Admin"

        return {
            "success": True,
            "data": {
                **user.to_dict(exclude=["password"]),
                "created_user": created_user,
                "updated_user": updated_user
            }
        }

    @staticmethod
    def get_all_users(page, per_page):
        pagination = UserDao.get_all_users(page, per_page)
        return pagination

    @staticmethod
    def search_users(name=None, email=None, role=None, start_date=None, end_date=None, page=1, per_page=10):
        pagination = UserDao.search_users(name, email, role, start_date, end_date, page, per_page)
        return pagination

    @staticmethod
    def lock_users(payload):
        users = UserDao.find_by_ids(payload.user_ids)

        if not users:
            raise BusinessException(
                field="user_ids",
                message="User not found"
            )

        UserDao.update_lock_status(users, payload.lock_flg)

    @staticmethod
    def create_user(payload, files, login_user_id):
        # Email & Name duplicate check
        user_exist = UserDao.find_by_email_or_name(payload.email, payload.name)
        if user_exist:
            if user_exist.email == payload.email:
                raise BusinessException(
                    field="email",
                    message="Email already exists"
                )
            if user_exist.name == payload.name:
                raise BusinessException(
                    field="name",
                    message="Name already exists"
                )

        # File validation
        profile = files.get("profile")
        profile_url = None

        if profile and not allowed_file:
            raise BusinessException(
                field="profile",
                message="Invalid file type"
            )

        if profile:
            upload_result = cloudinary.uploader.upload(
                profile,
                folder="users/profile",
                resource_type="image"
            )
            profile_url = upload_result["secure_url"]

        hashed_password = generate_password_hash(payload.password)

        user = UserDao.create_user(
            name=payload.name,
            email=payload.email,
            password=hashed_password,
            role=payload.role,
            phone=payload.phone,
            dob=payload.dob,
            address=payload.address,
            profile_path=profile_url,
            create_user_id=login_user_id
        )

        return user

    @staticmethod
    def update_user(user_id, payload, files, login_user_id):
        # check user exists
        user = UserDao.find_by_id(user_id)
        if not user:
            raise BusinessException(
                field="user_id",
                message="User not found"
            )

        # Email & Name duplicate check
        user_exist = UserDao.find_by_email_or_name_exclude_current_user(payload.email, payload.name, user.id)
        if user_exist:
            if user_exist.email == payload.email:
                raise BusinessException(
                    field="email",
                    message="Email already exists"
                )
            if user_exist.name == payload.name:
                raise BusinessException(
                    field="name",
                    message="Name already exists"
                )

        # File validation
        profile_url = None
        profile = files.get("profile")

        if profile:
            if not allowed_file(profile.filename):
                raise BusinessException(
                    field="profile",
                    message="Invalid file type"
                )

            upload_result = cloudinary.uploader.upload(
                profile,
                folder="users/profile",
                resource_type="image"
            )
            profile_url = upload_result["secure_url"]
            user.profile_path = profile_url

        user = UserDao.update_user(
            user,
            name=payload.name,
            email=payload.email,
            role=payload.role,
            phone=payload.phone,
            dob=payload.dob,
            address=payload.address,
            updated_user_id=login_user_id
        )

        return user

    @staticmethod
    def delete_user(user_ids, login_user_id):
        users = UserDao.find_by_ids(user_ids)

        if not users:
            raise BusinessException(
                field="user_ids",
                message="User not found"
            )

        UserDao.delete_users(users, login_user_id)
