import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class JWTConfig:

    # JWT connection parameters
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 30)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 7)))

    # JWT Cookie Settings
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_REFRESH_CSRF_COOKIE_NAME = "csrf_refresh_token"
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
