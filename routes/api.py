from app.controllers.usercontroller import UserController
from flask import Blueprint

# Auth blueprint
api = Blueprint("api", __name__)

api.get("/me")(UserController.get_current_user)