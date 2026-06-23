"""Public-facing pages, populated from the database."""

import os

from flask import Blueprint, abort, current_app, render_template, send_from_directory

from .models import AboutContent, Photo, Project, SiteSettings, TimelineEntry

public_bp = Blueprint("public", __name__)


def _ordered_projects():
    return Project.query.order_by(
        Project.is_featured.desc(), Project.display_order.asc(), Project.id.asc()
    ).all()


@public_bp.route("/")
def home():
    settings = SiteSettings.get()
    primary_photo = Photo.query.filter_by(is_primary=True).first()
    featured = Project.query.filter_by(is_featured=True).order_by(
        Project.display_order.asc()
    ).first()
    return render_template(
        "public/home.html",
        settings=settings,
        primary_photo=primary_photo,
        featured=featured,
    )


@public_bp.route("/about")
def about():
    settings = SiteSettings.get()
    about_content = AboutContent.get()
    photos = Photo.query.order_by(
        Photo.display_order.asc(), Photo.id.asc()
    ).all()
    return render_template(
        "public/about.html",
        settings=settings,
        about=about_content,
        photos=photos,
    )


@public_bp.route("/projects")
def projects():
    settings = SiteSettings.get()
    return render_template(
        "public/projects.html",
        settings=settings,
        projects=_ordered_projects(),
    )


@public_bp.route("/cv")
def cv():
    settings = SiteSettings.get()
    entries = TimelineEntry.query.order_by(
        TimelineEntry.display_order.asc(), TimelineEntry.id.asc()
    ).all()
    return render_template(
        "public/cv.html",
        settings=settings,
        entries=entries,
    )


@public_bp.route("/cv/download")
def cv_download():
    settings = SiteSettings.get()
    if not settings.cv_pdf_filename:
        abort(404)
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        settings.cv_pdf_filename,
        as_attachment=True,
        download_name="CV.pdf",
    )


@public_bp.route("/uploads/<path:filename>")
def uploads(filename):
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    if not os.path.isfile(os.path.join(upload_dir, filename)):
        abort(404)
    return send_from_directory(upload_dir, filename)
