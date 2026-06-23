"""Shared pytest fixtures.

Each test gets a fresh app backed by a throwaway SQLite file and a temporary
uploads directory, so tests never touch the developer's real data.
"""

import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / "test.db"
    upload_dir = tmp_path / "uploads"

    class _Config(TestConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        UPLOAD_FOLDER = str(upload_dir)

    application = create_app(_Config)
    yield application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(app):
    """A test client already logged into the admin dashboard."""
    test_client = app.test_client()
    test_client.post(
        "/admin/login", data={"password": app.config["ADMIN_PASSWORD"]}
    )
    return test_client


def login(client, password="test-password"):
    return client.post("/admin/login", data={"password": password})
