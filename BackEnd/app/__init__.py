"""Application factory for the portfolio CMS."""

import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import db


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    if os.environ.get("BEHIND_PROXY"):
        # Trust nginx's forwarded headers so redirects keep the public host/port.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    db.init_app(app)

    from .admin import admin_bp
    from .auth import auth_bp
    from .public import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        from .seed import seed_if_empty

        seed_if_empty()
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    return app
