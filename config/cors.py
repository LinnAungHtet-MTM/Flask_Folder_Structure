# config/cors.py

CORS_CONFIG = {
    "origins": ["http://localhost:5173"],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization", "skipAuth",],
    "supports_credentials": True,
}