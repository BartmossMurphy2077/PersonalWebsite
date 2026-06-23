"""Admin dashboard: CRUD for every editable piece of site content."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .auth import login_required
from .extensions import db
from .models import AboutContent, Photo, Project, SiteSettings, TimelineEntry
from .uploads import delete_upload, is_allowed_doc, is_allowed_image, save_upload

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _lines(raw):
    """Split a textarea value into a clean list (one item per non-empty line)."""
    return [line.strip() for line in (raw or "").splitlines() if line.strip()]


def _csv(raw):
    """Split a comma-separated value into a clean list."""
    return [item.strip() for item in (raw or "").split(",") if item.strip()]


@admin_bp.route("/")
@login_required
def dashboard():
    return redirect(url_for("admin.settings"))


# --- Site settings -------------------------------------------------------

@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    settings = SiteSettings.get()
    if request.method == "POST":
        settings.name = request.form.get("name", "").strip()
        settings.tagline = request.form.get("tagline", "").strip()
        settings.hero_bio = request.form.get("hero_bio", "").strip()
        settings.github_url = request.form.get("github_url", "").strip()
        settings.linkedin_url = request.form.get("linkedin_url", "").strip()
        settings.subtitle_lines = _lines(request.form.get("subtitle_lines"))

        responses = {}
        commands = request.form.getlist("cmd_name")
        replies = request.form.getlist("cmd_reply")
        for name, reply in zip(commands, replies):
            name = name.strip()
            if name:
                responses[name] = reply.strip()
        settings.terminal_responses = responses

        if not settings.name:
            flash("Name is required.", "error")
            return render_template("admin/settings.html", settings=settings)

        db.session.commit()
        flash("Settings saved.", "success")
        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html", settings=settings)


# --- Photos --------------------------------------------------------------

@admin_bp.route("/photos", methods=["GET", "POST"])
@login_required
def photos():
    if request.method == "POST":
        file = request.files.get("photo")
        if not file or not file.filename:
            flash("Choose an image to upload.", "error")
            return redirect(url_for("admin.photos"))
        if not is_allowed_image(file.filename):
            flash("Unsupported image type.", "error")
            return redirect(url_for("admin.photos"))

        filename = save_upload(file)
        make_primary = bool(request.form.get("is_primary"))
        if make_primary:
            Photo.query.update({Photo.is_primary: False})
        photo = Photo(
            filename=filename,
            alt_text=request.form.get("alt_text", "").strip(),
            is_primary=make_primary,
            display_order=Photo.query.count(),
        )
        db.session.add(photo)
        db.session.commit()
        flash("Photo uploaded.", "success")
        return redirect(url_for("admin.photos"))

    all_photos = Photo.query.order_by(
        Photo.display_order.asc(), Photo.id.asc()
    ).all()
    return render_template("admin/photos.html", photos=all_photos)


@admin_bp.route("/photos/<int:photo_id>/primary", methods=["POST"])
@login_required
def set_primary_photo(photo_id):
    photo = db.session.get(Photo, photo_id)
    if photo is None:
        flash("Photo not found.", "error")
        return redirect(url_for("admin.photos"))
    Photo.query.update({Photo.is_primary: False})
    photo.is_primary = True
    db.session.commit()
    flash("Primary photo updated.", "success")
    return redirect(url_for("admin.photos"))


@admin_bp.route("/photos/<int:photo_id>/delete", methods=["POST"])
@login_required
def delete_photo(photo_id):
    photo = db.session.get(Photo, photo_id)
    if photo is not None:
        delete_upload(photo.filename)
        db.session.delete(photo)
        db.session.commit()
        flash("Photo deleted.", "success")
    return redirect(url_for("admin.photos"))


# --- CV / experience -----------------------------------------------------

@admin_bp.route("/cv", methods=["GET"])
@login_required
def cv():
    settings = SiteSettings.get()
    entries = TimelineEntry.query.order_by(
        TimelineEntry.display_order.asc(), TimelineEntry.id.asc()
    ).all()
    return render_template("admin/cv.html", entries=entries, settings=settings)


@admin_bp.route("/cv/pdf", methods=["POST"])
@login_required
def upload_cv_pdf():
    settings = SiteSettings.get()
    file = request.files.get("cv_pdf")
    if not file or not file.filename:
        flash("Choose a PDF to upload.", "error")
        return redirect(url_for("admin.cv"))
    if not is_allowed_doc(file.filename):
        flash("CV must be a PDF.", "error")
        return redirect(url_for("admin.cv"))

    if settings.cv_pdf_filename:
        delete_upload(settings.cv_pdf_filename)
    settings.cv_pdf_filename = save_upload(file)
    db.session.commit()
    flash("CV uploaded.", "success")
    return redirect(url_for("admin.cv"))


@admin_bp.route("/cv/entries", methods=["POST"])
@login_required
def create_timeline_entry():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Title is required.", "error")
        return redirect(url_for("admin.cv"))
    entry = TimelineEntry(
        title=title,
        organization=request.form.get("organization", "").strip(),
        start_date=request.form.get("start_date", "").strip(),
        end_date=request.form.get("end_date", "").strip(),
        bullets=_lines(request.form.get("bullets")),
        display_order=TimelineEntry.query.count(),
    )
    db.session.add(entry)
    db.session.commit()
    flash("Timeline entry added.", "success")
    return redirect(url_for("admin.cv"))


@admin_bp.route("/cv/entries/<int:entry_id>/edit", methods=["GET", "POST"])
@login_required
def edit_timeline_entry(entry_id):
    entry = db.session.get(TimelineEntry, entry_id)
    if entry is None:
        flash("Entry not found.", "error")
        return redirect(url_for("admin.cv"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return render_template("admin/cv_entry.html", entry=entry)
        entry.title = title
        entry.organization = request.form.get("organization", "").strip()
        entry.start_date = request.form.get("start_date", "").strip()
        entry.end_date = request.form.get("end_date", "").strip()
        entry.bullets = _lines(request.form.get("bullets"))
        entry.display_order = int(request.form.get("display_order") or 0)
        db.session.commit()
        flash("Entry updated.", "success")
        return redirect(url_for("admin.cv"))
    return render_template("admin/cv_entry.html", entry=entry)


@admin_bp.route("/cv/entries/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete_timeline_entry(entry_id):
    entry = db.session.get(TimelineEntry, entry_id)
    if entry is not None:
        db.session.delete(entry)
        db.session.commit()
        flash("Entry deleted.", "success")
    return redirect(url_for("admin.cv"))


# --- Projects ------------------------------------------------------------

@admin_bp.route("/projects", methods=["GET"])
@login_required
def projects():
    all_projects = Project.query.order_by(
        Project.display_order.asc(), Project.id.asc()
    ).all()
    return render_template("admin/projects.html", projects=all_projects)


def _apply_project_form(project):
    project.title = request.form.get("title", "").strip()
    project.description = request.form.get("description", "").strip()
    project.tech_tags = _csv(request.form.get("tech_tags"))
    project.github_url = request.form.get("github_url", "").strip()
    project.demo_url = request.form.get("demo_url", "").strip()
    project.is_featured = bool(request.form.get("is_featured"))
    project.display_order = int(request.form.get("display_order") or 0)

    file = request.files.get("thumbnail")
    if file and file.filename:
        if not is_allowed_image(file.filename):
            return "Unsupported thumbnail type."
        if project.thumbnail_filename:
            delete_upload(project.thumbnail_filename)
        project.thumbnail_filename = save_upload(file)
    return None


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def create_project():
    if request.method == "POST":
        project = Project()
        if not request.form.get("title", "").strip():
            flash("Title is required.", "error")
            return render_template("admin/project_form.html", project=project, mode="new")
        error = _apply_project_form(project)
        if error:
            flash(error, "error")
            return render_template("admin/project_form.html", project=project, mode="new")
        db.session.add(project)
        db.session.commit()
        flash("Project created.", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html", project=Project(), mode="new")


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = db.session.get(Project, project_id)
    if project is None:
        flash("Project not found.", "error")
        return redirect(url_for("admin.projects"))
    if request.method == "POST":
        if not request.form.get("title", "").strip():
            flash("Title is required.", "error")
            return render_template("admin/project_form.html", project=project, mode="edit")
        error = _apply_project_form(project)
        if error:
            flash(error, "error")
            return render_template("admin/project_form.html", project=project, mode="edit")
        db.session.commit()
        flash("Project updated.", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html", project=project, mode="edit")


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    project = db.session.get(Project, project_id)
    if project is not None:
        delete_upload(project.thumbnail_filename)
        db.session.delete(project)
        db.session.commit()
        flash("Project deleted.", "success")
    return redirect(url_for("admin.projects"))


# --- About ---------------------------------------------------------------

@admin_bp.route("/about", methods=["GET", "POST"])
@login_required
def about():
    about_content = AboutContent.get()
    if request.method == "POST":
        about_content.long_bio = request.form.get("long_bio", "").strip()
        about_content.interests = request.form.get("interests", "").strip()
        db.session.commit()
        flash("About content saved.", "success")
        return redirect(url_for("admin.about"))
    return render_template("admin/about.html", about=about_content)
