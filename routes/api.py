from app.controllers.postcontroller import PostController
from app.controllers.usercontroller import UserController
from flask import Blueprint

# Auth blueprint
api = Blueprint("api", __name__)

# User
api.get("/users")(UserController.get_all_users)
api.get("/login_user")(UserController.get_login_user)
api.get("/users/<int:user_id>")(UserController.get_user_by_id)
api.put("/users/lock")(UserController.lock_users)
api.post("/users/search")(UserController.search_users)
api.post("/users/create")(UserController.create_user)
api.put("/users/<int:user_id>")(UserController.update_user)
api.delete("/users/delete")(UserController.delete_user)
api.put("/users/<int:user_id>/change_password")(UserController.change_password)

# Post
api.get("/posts")(PostController.get_all_posts)
api.get("/posts/<int:post_id>")(PostController.get_post_by_id)
api.post("/posts/search")(PostController.search_posts)
api.post("/posts/create")(PostController.create_post)
api.put("/posts/<int:post_id>")(PostController.update_post)
api.delete("/posts/delete")(PostController.delete_post)
api.post("/posts/export")(PostController.export_post_csv)
api.post("/posts/import")(PostController.import_post_csv)
