"""Minimal single-password session authentication for the admin dashboard."""

from functools import wraps
from urllib.parse import urlparse

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

auth_bp = Blueprint("auth", __name__)

SESSION_KEY = "is_admin"


def _safe_next(target):
    """Only allow same-site relative redirects, to block open-redirect abuse."""
    if not target:
        return None
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc:
        return None
    if not target.startswith("/"):
        return None
    return target


def login_required(view):
    """Redirect unauthenticated users to the login page."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get(SESSION_KEY):
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if session.get(SESSION_KEY):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == current_app.config["ADMIN_PASSWORD"]:
            session[SESSION_KEY] = True
            next_url = _safe_next(request.args.get("next")) or url_for(
                "admin.dashboard"
            )
            return redirect(next_url)
        flash("Incorrect password.", "error")

    return render_template("admin/login.html")


@auth_bp.route("/admin/logout", methods=["POST"])
def logout():
    session.pop(SESSION_KEY, None)
    flash("Logged out.", "success")
    return redirect(url_for("auth.login"))
