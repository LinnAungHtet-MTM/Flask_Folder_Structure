from app.dao.password_reset_dao import PasswordResetDao
from app.dao.userdao import UserDao
from app.services import authservice
from app.services.authservice import AuthService
from flask import request, jsonify
from flask_jwt_extended import decode_token
from pydantic import ValidationError
from app.requests.authrequest import ForgotPasswordRequest, LoginRequest, ResetPasswordRequest, VerifyResetTokenRequest


class AuthController:
    def login():
        try:
            payload = LoginRequest(**request.get_json())
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        result = AuthService.login(payload)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [
                            result["field"]
                        ],
                        "success": False,
                        "msg": result["message"]
                    }
                ]
            ), 422

        return jsonify({
            "success": True,
            "data": result["data"],
            "message": "Login successful"
        }), 200

    @staticmethod
    def forgot_password():
        try:
            payload = ForgotPasswordRequest(**request.get_json())
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        result = AuthService.forgot_password(payload)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [
                            result["field"]
                        ],
                        "success": False,
                        "msg": result["message"]
                    }
                ]
            ), 422

        return jsonify({
            "success": True,
            "data": result["data"],
            "message": "Reset password link send to your email"
        }), 200

    @staticmethod
    def verify_reset_token():
        try:
            payload = VerifyResetTokenRequest(**request.args)
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        token = payload.token

        result = AuthService.verify_reset_token(token)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [
                            result["field"]
                        ],
                        "success": False,
                        "msg": result["message"]
                    }
                ]
            ), 401

        return jsonify({
            "success": True,
            "message": "Valid Token"
        }), 200

    @staticmethod
    def reset_password():
        try:
            payload = ResetPasswordRequest(**request.get_json())
        except ValidationError as e:
            print(e.errors())
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        result = AuthService.reset_password(payload)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [result["field"]],
                        "success": False,
                        "msg": result["message"]
                    }
                ]
            ), 401

        return jsonify({
            "success": True,
            "message": "Password Updated Successfully"
        }), 200



    # @staticmethod
    # def reset_password():
    #     data = request.get_json()
    #     token = data.get("token")
    #     new_password = data.get("password")

    #     email = AuthService.verify_reset_token(token)
    #     if not email:
    #         return jsonify({"success": False, "message": "Invalid or expired token"}), 400

    #     user = UserDao.find_by_email(email)
    #     user.password = generate_password_hash(new_password)
    #     user.save()  # or db.session.commit()
    #     PasswordResetDao.delete_by_token(token)

    #     return jsonify({"success": True, "message": "Password updated successfully"}), 200
