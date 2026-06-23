"""Helpers for validating and persisting uploaded files to disk."""

import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def _extension(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def is_allowed_image(filename):
    return _extension(filename) in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def is_allowed_doc(filename):
    return _extension(filename) in current_app.config["ALLOWED_DOC_EXTENSIONS"]


def save_upload(file_storage):
    """Persist an uploaded file under a collision-proof name; return the name.

    The original filename is sanitised and prefixed with a short random token
    so two uploads with the same name never overwrite each other.
    """
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    original = secure_filename(file_storage.filename) or "file"
    unique = f"{uuid.uuid4().hex[:8]}_{original}"
    file_storage.save(os.path.join(upload_dir, unique))
    return unique


def delete_upload(filename):
    """Remove a previously stored upload if it exists. Best-effort."""
    if not filename:
        return
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    try:
        os.remove(path)
    except OSError:
        pass
