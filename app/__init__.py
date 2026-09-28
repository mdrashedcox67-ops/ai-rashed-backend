from __future__ import annotations

from flask import Flask

from app.config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import bp

    app.register_blueprint(bp)

    return app
