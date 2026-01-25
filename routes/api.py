from app.controllers.usercontroller import UserController
from flask import Blueprint

# Auth blueprint
api = Blueprint("api", __name__)

api.get("/users")(UserController.get_all_users)
api.get("/login_user")(UserController.get_login_user)
api.post("/users/search")(UserController.search_users)
api.put("/users/lock")(UserController.lock_users)
api.post("/users/create")(UserController.create_user)
api.get("users/<int:user_id>")(UserController.get_user_by_id)
api.put("users/<int:user_id>")(UserController.update_user)
api.delete("users/delete")(UserController.delete_user)