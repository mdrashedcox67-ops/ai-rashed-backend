from functools import wraps
from flask import request, jsonify

def require_app_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function
