"""Application configuration.

Values come from environment variables (loaded from a local .env in
development) so that secrets never live in the repository.
"""

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent  # the BackEnd/ directory


class Config:
    # Fall back to a random per-process key so sessions are never signed with a
    # predictable secret. Set SECRET_KEY in .env to keep sessions across restarts.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'portfolio.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload cap

    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_DOC_EXTENSIONS = {"pdf"}


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret"
    ADMIN_PASSWORD = "test-password"
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # in-memory
    WTF_CSRF_ENABLED = False
