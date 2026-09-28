from __future__ import annotations

from functools import wraps
from flask import current_app, request
from app.errors import make_error_response


def require_app_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return make_error_response("Missing or invalid Authorization header", 401)

        token = auth_header.split("Bearer ", 1)[1].strip()
        allowed_tokens = current_app.config.get("APP_TOKENS", [])

        if not allowed_tokens or token not in allowed_tokens:
            return make_error_response("Unauthorized token", 403)

        return f(*args, **kwargs)

    return decorated_function
