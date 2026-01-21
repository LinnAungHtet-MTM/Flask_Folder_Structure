from app.services.authservice import AuthService
from app.services.userservice import UserService
from flask import request, jsonify
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.requests.authrequest import LoginRequest


class UserController:
    @staticmethod
    @jwt_required()
    def get_current_user():
        user_id = int(get_jwt_identity())
        user = UserService.get_login_user(user_id)

        return jsonify({
            "success": True,
            "data": user.to_dict(exclude=["password"]),
        }), 200
