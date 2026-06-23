"""Database models for the portfolio CMS.

The schema is intentionally small: two singletons (SiteSettings, AboutContent)
plus three content collections (Photo, TimelineEntry, Project). JSON columns
hold the variable-length bits (subtitle lines, bullet points, tech tags) so the
admin forms stay simple.
"""

from datetime import datetime, timezone

from .extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


class SiteSettings(db.Model):
    """Global, single-row site configuration."""

    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, default="Your Name")
    tagline = db.Column(db.String(255), nullable=False, default="")
    hero_bio = db.Column(db.Text, nullable=False, default="")
    github_url = db.Column(db.String(255), nullable=False, default="")
    linkedin_url = db.Column(db.String(255), nullable=False, default="")
    subtitle_lines = db.Column(db.JSON, nullable=False, default=list)
    terminal_responses = db.Column(db.JSON, nullable=False, default=dict)
    cv_pdf_filename = db.Column(db.String(255), nullable=True)

    @classmethod
    def get(cls):
        """Return the singleton row, creating it on first access."""
        settings = cls.query.first()
        if settings is None:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings


class AboutContent(db.Model):
    """Single-row long-form content for the About page."""

    __tablename__ = "about_content"

    id = db.Column(db.Integer, primary_key=True)
    long_bio = db.Column(db.Text, nullable=False, default="")
    interests = db.Column(db.Text, nullable=False, default="")

    @classmethod
    def get(cls):
        about = cls.query.first()
        if about is None:
            about = cls()
            db.session.add(about)
            db.session.commit()
        return about


class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(255), nullable=False, default="")
    is_primary = db.Column(db.Boolean, nullable=False, default=False)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=_utcnow)


class TimelineEntry(db.Model):
    __tablename__ = "timeline_entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255), nullable=False, default="")
    start_date = db.Column(db.String(64), nullable=False, default="")
    end_date = db.Column(db.String(64), nullable=True)  # null/"" => present
    bullets = db.Column(db.JSON, nullable=False, default=list)
    display_order = db.Column(db.Integer, nullable=False, default=0)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    tech_tags = db.Column(db.JSON, nullable=False, default=list)
    github_url = db.Column(db.String(255), nullable=True)
    demo_url = db.Column(db.String(255), nullable=True)
    thumbnail_filename = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    display_order = db.Column(db.Integer, nullable=False, default=0)
