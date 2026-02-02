from app.core.transactional import transactional
from app.requests.userrequest import ChangePasswordRequest, CreateUserRequest, LockUsersRequest, UpdateUserRequest, UserSearchRequest
from app.services.userservice import UserService
from flask import request, jsonify
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middlewares.role_permission import role_permission

class UserController:

    @staticmethod
    @jwt_required()
    def get_login_user():
        user_id = int(get_jwt_identity())
        result = UserService.get_user_by_id(user_id)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [result["field"]],
                        "msg": result["message"]
                    }
                ]
            ), 400

        return jsonify({
            "success": True,
            "data": result["data"],
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    def get_all_users():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        pagination = UserService.get_all_users(page, per_page)

        return jsonify({
            "success": True,
            "data": [
                user.to_dict(exclude=["password"])
                for user in pagination.items
            ],
            "meta": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "total_pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    def search_users():
        try:
            payload = UserSearchRequest(**(request.get_json() or {}))
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = UserService.search_users(
            name=payload.name,
            email=payload.email,
            role=payload.role,
            start_date=payload.start_date,
            end_date=payload.end_date,
            page=page,
            per_page=per_page
        )

        return jsonify({
            "success": True,
            "data": [
                user.to_dict(exclude=["password"])
                for user in pagination.items
            ],
            "meta": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "total_pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    @transactional
    def lock_users():
        payload = LockUsersRequest(**request.get_json())
        UserService.lock_users(payload)

        return jsonify({
            "success": True,
            "message": "Account updated successfully"
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    @transactional
    def create_user():
        payload = CreateUserRequest(**request.form)
        login_user_id = int(get_jwt_identity())
        user = UserService.create_user(payload, request.files, login_user_id)

        return jsonify({
            "success": True,
            "data": user.to_dict(exclude=["password"]),
            "message": "User created successfully"
        }), 201

    @staticmethod
    @jwt_required()
    @role_permission
    def get_user_by_id(user_id):
        result = UserService.get_user_by_id(user_id)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [result["field"]],
                        "msg": result["message"]
                    }
                ]
            ), 400

        return jsonify({
            "success": True,
            "data": result["data"],
        }), 200

    @staticmethod
    @jwt_required()
    # @role_permission
    @transactional
    def update_user(user_id):
        payload = UpdateUserRequest(**request.form)
        login_user_id = int(get_jwt_identity())
        user = UserService.update_user(
            user_id, payload, request.files, login_user_id)

        return jsonify({
            "success": True,
            "data": user.to_dict(exclude=["password"]),
            "message": "User updated successfully"
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    @transactional
    def delete_user():
        payload = request.get_json()
        login_user_id = int(get_jwt_identity())
        UserService.delete_user(payload["user_ids"], login_user_id)

        return jsonify({
            "success": True,
            "message": "User Deleted Successfully"
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    @transactional
    def change_password(user_id):
        payload = ChangePasswordRequest(**request.get_json())
        UserService.change_password(user_id, payload)

        return jsonify({
            "success": True,
            "message": "Password Updated Successfully"
        }), 200
