from datetime import datetime, timedelta
from app.dao.password_reset_dao import PasswordResetDao
from app.extension import db
from app.utils.email_util import send_email
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, decode_token
from app.dao.userdao import UserDao
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()


class AuthService:

    @staticmethod
    def login(payload):
        user = UserDao.find_by_email(payload.email)

        if not user:
            return {
                "field": "email",
                "success": False,
                "message": "Selected Email Address doesn't exist"
            }

        if not check_password_hash(user.password, payload.password):
            return {
                "field": "password",
                "success": False,
                "message": "Invalid credentials"
            }

        # update last login
        user.last_login_at = datetime.utcnow()
        db.session.commit()

        token = create_access_token(identity=str(user.id))

        return {
            "success": True,
            "data": {
                "access_token": token,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            }
        }

    @staticmethod
    def forgot_password(payload):
        user = UserDao.find_by_email(payload.email)
        if not user:
            return {
                "field": "email",
                "success": False,
                "message": "Selected Email Address doesn't exist"
            }

        token = AuthService.generate_reset_token(payload.email)
        token_hash = AuthService.hash_token(token)
        PasswordResetDao.create(payload.email, token_hash)

        reset_link = f"http://localhost:5173/reset-password?token={token}"
        html = f"""
        <p>Click the button below to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        <p>If you didn’t request this, ignore this email.</p>
        """

        text = f"Reset your password using this link:\n{reset_link}"
        send_email(payload.email, "Reset Password", text, html)

        return {
            "success": True,
            "data": {
                "reset_password_link": reset_link,
            }
        }

    @staticmethod
    def generate_reset_token(email: str):
        token = create_access_token(
            identity=email,
            expires_delta=timedelta(minutes=10),
            additional_claims={"type": "reset"}
        )
        return token

    @staticmethod
    def verify_reset_token(token: str):
        if not token:
            return {
                "field": "token",
                "success": False,
                "message": "Token required"
            }

        try:
            decoded = decode_token(token)
        except Exception:
            return {
                "field": "token",
                "success": False,
                "message": "Invalid or Expire token"
            }

        if decoded.get("type") != "reset":
            return {
                "field": "token",
                "success": False,
                "message": "Invalid token"
            }

        token_hash = AuthService.hash_token(token)

        reset = PasswordResetDao.find_valid(
            email=decoded["sub"],
            token_hash=token_hash
        )

        if not reset:
            return {
                "field": "token",
                "success": False,
                "message": "Invalid token or already used"
            }

        return {
            "success": True,
        }

    @staticmethod
    def reset_password(payload):
        try:
            decoded = decode_token(payload.token)
        except Exception:
            return {
                "field": "token",
                "success": False,
                "message": "Invalid or expired token"
            }

        if decoded.get("type") != "reset":
            return {
                "field": "token",
                "success": False,
                "message": "Invalid token"
            }

        token_hash = AuthService.hash_token(payload.token)

        reset = PasswordResetDao.find_valid(
            email=decoded["sub"],
            token_hash=token_hash
        )

        if not reset:
            return {
                "field": "token",
                "success": False,
                "message": "Token already used or invalid"
            }

        # 🔹 Update user password
        user = UserDao.find_by_email(decoded["sub"])
        if not user:
            return {
                "field": "email",
                "success": False,
                "message": "User not found"
            }

        user.password = generate_password_hash(payload.password)
        db.session.commit()

        # 🔹 Invalidate token
        reset.deleted_at = datetime.utcnow()
        db.session.commit()

        return {"success": True}


    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
