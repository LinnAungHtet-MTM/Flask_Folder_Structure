from app.models.user import User
from app.requests.userrequest import CreateUserRequest, LockUsersRequest, UpdateUserRequest, UserSearchRequest
from app.services.authservice import AuthService
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
            name = payload.name,
            email = payload.email,
            role = payload.role,
            start_date = payload.start_date,
            end_date = payload.end_date,
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
    def lock_users():
        try:
            payload = LockUsersRequest(**request.get_json())
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        result = UserService.lock_users(payload)

        if not result["success"]:
            return jsonify(
                [
                    {"loc": ["user_ids"], "msg": result["message"]}
                ]
            ), 400

        return jsonify({
            "success": True,
            "message": result["message"]
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    def create_user():
        try:
            payload = CreateUserRequest(**request.form)
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        login_user_id = int(get_jwt_identity())

        result = UserService.create_user(payload, request.files, login_user_id)

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
            "data": result["data"].to_dict(exclude=["password"]),
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
    @role_permission
    def update_user(user_id):
        try:
            payload = UpdateUserRequest(**request.form)
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        login_user_id = int(get_jwt_identity())

        result = UserService.update_user(user_id, payload, request.files, login_user_id)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [result["field"]],
                        "msg": result["message"]
                    }
                ]
            ), result["status"]

        return jsonify({
            "success": True,
            "data": result["data"].to_dict(exclude=["password"]),
            "message": "User updated successfully"
        }), 200

    @staticmethod
    @jwt_required()
    @role_permission
    def delete_user():
        try:
            payload = request.get_json()
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        result = UserService.delete_user(payload["user_ids"])

        if not result["success"]:
            return jsonify(
                [
                    {"loc": ["user_ids"], "msg": result["message"]}
                ]
            ), 400

        return jsonify({
            "success": True,
            "message": result["message"]
        }), 200