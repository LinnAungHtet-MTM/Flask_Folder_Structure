from app.core.transactional import transactional
from app.services.authservice import AuthService
from flask import request, jsonify
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies
from app.requests.authrequest import ForgotPasswordRequest, LoginRequest, ResetPasswordRequest, VerifyResetTokenRequest


class AuthController:

    # Login
    @staticmethod
    @transactional
    def login():
        payload = LoginRequest(**request.get_json())
        result = AuthService.login(payload)

        response = jsonify({
            "success": True,
            "message": "Login successful",
            "data": {
                "access_token": result["access_token"]
            }
        })

        if payload.remember:
            # persistent cookie (30 days)
            set_refresh_cookies(
                response,
                result["refresh_token"],
                max_age=int(result["refresh_expires"].total_seconds())
            )
        else:
            # session cookie (browser close = logout)
            set_refresh_cookies(
                response,
                result["refresh_token"]
            )

        return response, 200


    # Generate Refresh Token
    @staticmethod
    @jwt_required(refresh=True, locations=["cookies"])
    def refresh():
        user_id = int(get_jwt_identity())
        result = AuthService.refresh_token(user_id)

        if not result["success"]:
            return jsonify({
                "success": False,
                "message": result["message"]
            }), 401

        return jsonify({
            "success": True,
            "message": "Access token refreshed",
            "access_token": result["data"]["access_token"]
        }), 200


    # Forgot Password
    @staticmethod
    @transactional
    def forgot_password():
        payload = ForgotPasswordRequest(**request.get_json())
        AuthService.forgot_password(payload)

        return jsonify({
            "success": True,
            "message": "Reset password link send to your email"
        }), 200


    # Verify Reset Toeken
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


    # Reset Password
    @staticmethod
    @transactional
    def reset_password():
        payload = ResetPasswordRequest(**request.get_json())
        AuthService.reset_password(payload)

        return jsonify({
            "success": True,
            "message": "Password Updated Successfully"
        }), 200


    # Logout
    @staticmethod
    @jwt_required()
    def logout():
        response = jsonify({
            "success": True,
            "message": "Logged out successfully"
        })

        unset_jwt_cookies(response)
        return response, 200
