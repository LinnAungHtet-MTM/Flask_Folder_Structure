from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_permission(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        if claims.get("role"):
            return jsonify(
                [{
                    "loc": ["role"],
                    "msg": "Admin access required"
                }]
            ), 403

        return fn(*args, **kwargs)
    return wrapper
