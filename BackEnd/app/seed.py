"""Seed the database with content carried over from the original single-page
site so the CMS is never empty on first run."""

from .extensions import db
from .models import AboutContent, Project, SiteSettings, TimelineEntry


def seed_if_empty():
    """Populate baseline content when the database has no site settings yet."""
    if SiteSettings.query.first() is not None:
        return

    settings = SiteSettings(
        name="Hugo Kotuc",
        tagline="Software & AI Engineer",
        hero_bio=(
            "I am a 3rd year student at IE University with experience from IT "
            "companies, where I worked on Retrieval-Augmented Generation (RAG) "
            "solutions and AI agents."
        ),
        github_url="https://github.com/BartmossMurphy2077/",
        linkedin_url="https://www.linkedin.com/in/hugo-kotuc-b0baa8311/",
        subtitle_lines=[
            "Building RAG pipelines",
            "3rd year at IE University",
            "Wrangling AI agents",
            "Probably debugging something",
        ],
        terminal_responses={
            "whoami": "Hugo Kotuc - Software & AI Engineer",
            "skills": "Java, Python, C, AI Agents, RAG Solutions",
            "projects": "Type 'View Projects' or visit /projects to see them all.",
            "help": "Available commands: whoami, skills, projects, help",
        },
    )
    db.session.add(settings)

    about = AboutContent(
        long_bio=(
            "I'm Hugo, a 3rd year student at IE University. I spend my time "
            "building AI systems - lately a lot of Retrieval-Augmented "
            "Generation and agentic tooling at the Kempelen Institute of "
            "Technology. I like turning messy problems into clean, working "
            "software."
        ),
        interests=(
            "Outside of code: tinkering with side projects, learning new "
            "languages (both human and programming), and a healthy amount of "
            "coffee."
        ),
    )
    db.session.add(about)

    db.session.add(
        TimelineEntry(
            title="BSc Student",
            organization="IE University",
            start_date="2023",
            end_date="",
            bullets=["3rd year student", "Focus on software and AI"],
            display_order=0,
        )
    )
    db.session.add(
        TimelineEntry(
            title="AI Engineer",
            organization="Kempelen Institute of Technology",
            start_date="2024",
            end_date="",
            bullets=[
                "Built Retrieval-Augmented Generation (RAG) solutions",
                "Developed AI agents",
            ],
            display_order=1,
        )
    )

    db.session.add(
        Project(
            title="Personal Website CMS",
            description=(
                "This very site - a Flask + SQLite portfolio with a custom "
                "admin dashboard for managing projects, photos, and CV content."
            ),
            tech_tags=["Python", "Flask", "SQLite", "JavaScript"],
            github_url="https://github.com/BartmossMurphy2077/PersonalWebsite",
            demo_url="",
            is_featured=True,
            display_order=0,
        )
    )

    db.session.commit()
