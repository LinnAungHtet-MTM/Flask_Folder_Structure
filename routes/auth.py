from flask import Blueprint
from app.controllers.authcontroller import AuthController

# Auth blueprint
auth = Blueprint("auth", __name__)

auth.post("/login")(AuthController.login)
auth.post("/refresh")(AuthController.refresh)
auth.post("/forgot-password")(AuthController.forgot_password)
auth.get("/verify-reset-token")(AuthController.verify_reset_token)
auth.post("/reset-password")(AuthController.reset_password)
auth.post("/logout")(AuthController.logout)