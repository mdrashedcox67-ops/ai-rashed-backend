from __future__ import annotations

from typing import Any

from flask import jsonify


def make_error_response(message: str, status_code: int, details: Any = None):
    payload = {
        "error": {
            "message": message,
            "status_code": status_code,
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return jsonify(payload), status_code
