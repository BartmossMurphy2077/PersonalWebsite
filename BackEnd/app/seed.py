"""Seed the database with Hugo's real content (sourced from his LinkedIn and
GitHub) so the CMS is never empty on first run.

Two entry points:

- ``seed_if_empty()`` populates a brand-new database once.
- ``refresh_content()`` replaces settings/about/timeline/projects with the
  current seed data on an existing database, preserving uploaded photos, the
  CV PDF, and project thumbnails (matched by title).
"""

from .extensions import db
from .models import AboutContent, Project, SiteSettings, TimelineEntry


def _settings_data():
    return dict(
        name="Hugo Kotuc",
        tagline="Computer Science & AI Student · AI Research Intern",
        hero_bio=(
            "Computer Science & AI student at IE University and research intern "
            "at the Kempelen Institute of Intelligent Technologies (KInIT). I "
            "build AI systems - lately Retrieval-Augmented Generation, "
            "LLM security tooling, and agentic workflows - and like turning "
            "messy problems into clean, working software."
        ),
        github_url="https://github.com/BartmossMurphy2077",
        linkedin_url="https://www.linkedin.com/in/hugo-kotuc-b0baa8311/",
        subtitle_lines=[
            "Researching AI at KInIT",
            "CS & AI @ IE University",
            "RAG & prompt-injection tinkerer",
            "Slang-aware NLP experimenter",
            "2nd place @ Talent Arena hackathon",
            "Probably debugging something",
        ],
        terminal_responses={
            "whoami": (
                "Hugo Kotuc - CS & AI student @ IE University, "
                "AI research intern @ KInIT"
            ),
            "skills": (
                "Python, PyTorch, Transformers, FastAPI, React, Java, C, "
                "AI Agents, RAG, Docker, CI/CD, Git"
            ),
            "projects": (
                "PromptInjectionTester, slang-aware sentiment analysis, "
                "GPT Challenge, this site - see /projects"
            ),
            "languages": (
                "Slovak (native), English (native), Spanish (working), "
                "Mandarin (basic)"
            ),
            "help": "Available commands: whoami, skills, projects, languages, help",
        },
    )


def _about_data():
    return dict(
        long_bio=(
            "I'm Hugo, a Computer Science & Artificial Intelligence student at "
            "IE University in Segovia, Spain, originally from Bratislava, "
            "Slovakia.\n\n"
            "I'm currently a research intern at the Kempelen Institute of "
            "Intelligent Technologies (KInIT), a nonprofit AI research "
            "institute, where I work on Retrieval-Augmented Generation and "
            "agentic tooling. Previously I interned at Vacuumlabs, where I "
            "researched RAG, cleaned up CRM data, and helped improve their AI "
            "academy.\n\n"
            "I like building things and competing - my team placed 2nd at a "
            "hackathon and represented at Talent Arena and MWC in Barcelona. "
            "Lately I've been deep in NLP research: slang-aware sentiment "
            "analysis with BERT and BERTweet, and building transformer "
            "architectures from scratch to understand them properly."
        ),
        interests=(
            "Languages: Slovak (native), English (native), Spanish (working "
            "proficiency), Mandarin (elementary).\n\n"
            "Certifications: EA Software Engineering Job Simulation (Forage), "
            "Learning Docker, React Essential Training, and Git Essential "
            "Training.\n\n"
            "Outside of code: hackathons, open-source events like FOSDEM, and "
            "learning new languages - both human and programming."
        ),
    )


def _timeline_data():
    return [
        dict(
            title="Research Intern",
            organization="Kempelen Institute of Intelligent Technologies (KInIT)",
            start_date="Aug 2025",
            end_date="",
            bullets=[
                "AI research at a nonprofit intelligent-technologies institute",
                "Working on Retrieval-Augmented Generation and agentic tooling",
                "Evaluating LLM robustness, including prompt-injection resistance",
            ],
            display_order=0,
        ),
        dict(
            title="Student Intern",
            organization="Vacuumlabs",
            start_date="Jun 2024",
            end_date="Aug 2024",
            bullets=[
                "Researched Retrieval-Augmented Generation (RAG)",
                "Cleaned up CRM data and reported progress frequently",
                "Gave feedback to improve the company's AI academy",
            ],
            display_order=1,
        ),
        dict(
            title="BSc Computer Science & Artificial Intelligence",
            organization="IE University, Segovia",
            start_date="2023",
            end_date="2027",
            bullets=[
                "Computer Science and Artificial Intelligence degree",
                "Coursework spanning NLP, machine learning, and DevOps",
                "Active in hackathons and the campus tech community",
            ],
            display_order=2,
        ),
        dict(
            title="IB Diploma (IBDP) & IGCSE",
            organization="British International School of Bratislava (Nord Anglia)",
            start_date="2016",
            end_date="2023",
            bullets=[
                "IB Computer Science HL, Economics HL, Math HL",
                "Coding club and Eco committee",
            ],
            display_order=3,
        ),
    ]


def _project_data():
    """Curated selection of Hugo's public GitHub work, best first."""
    return [
        dict(
            title="PromptInjectionTester",
            description=(
                "A harness for evaluating LLM prompt-injection resistance: "
                "datasets of injection attempts are fed to a tester model and "
                "an auditor model classifies each exchange as BREACH or SAFE, "
                "producing a security scorecard for the system under test."
            ),
            tech_tags=["Python", "LLMs", "AI Security"],
            github_url="https://github.com/BartmossMurphy2077/PromptInjectionTester",
            demo_url="",
            is_featured=True,
            display_order=0,
        ),
        dict(
            title="Personal Website CMS",
            description=(
                "This very site - a Flask + SQLite portfolio with a custom "
                "admin dashboard for managing projects, photos, and CV "
                "content, terminal-themed easter eggs, and Docker deployment."
            ),
            tech_tags=["Python", "Flask", "SQLite", "Docker", "JavaScript"],
            github_url="https://github.com/BartmossMurphy2077/PersonalWebsite",
            demo_url="",
            is_featured=False,
            display_order=1,
        ),
        dict(
            title="Slang-Aware Sentiment Analysis",
            description=(
                "Full NLP research pipeline for sentiment analysis with "
                "slang-aware experimentation: data collection and cleaning, "
                "preprocessing with slang feature signals, BERT-base and "
                "BERTweet modeling with a GPT baseline, and multi-seed "
                "evaluation with paired significance tests."
            ),
            tech_tags=["Python", "PyTorch", "Transformers", "NLP"],
            github_url="https://github.com/BartmossMurphy2077/NLP_Final_project",
            demo_url="",
            is_featured=False,
            display_order=2,
        ),
        dict(
            title="GPT Challenge",
            description=(
                "Transformer internals built from scratch: batching, core "
                "attention modules, BERT/BART model variants, and a GPT "
                "skeleton with training utilities - an exercise in "
                "understanding the architecture end to end."
            ),
            tech_tags=["Python", "PyTorch", "Transformers"],
            github_url="https://github.com/BartmossMurphy2077/GPTchallenge",
            demo_url="",
            is_featured=False,
            display_order=3,
        ),
        dict(
            title="Expense Management System",
            description=(
                "A full-stack expense tracker built for a DevOps course: "
                "FastAPI + SQLAlchemy backend, React + Chart.js frontend, "
                "JWT authentication, tagged expenses with spending analytics, "
                "all containerised with Docker Compose."
            ),
            tech_tags=["FastAPI", "React", "Docker", "SQLite", "JWT"],
            github_url="https://github.com/BartmossMurphy2077/ExpenseManagementSystem",
            demo_url="",
            is_featured=False,
            display_order=4,
        ),
        dict(
            title="Well-Being Visualisation",
            description=(
                "Reproducible data-analysis package over Gapminder wellness "
                "datasets - builds a data audit and an insights report with "
                "charts from raw CSVs in a single command."
            ),
            tech_tags=["Python", "Jupyter", "Pandas", "Data Analysis"],
            github_url="https://github.com/BartmossMurphy2077/WellBeingVisualisation",
            demo_url="",
            is_featured=False,
            display_order=5,
        ),
    ]


def _insert_all():
    """Insert fresh rows for every seeded table (no deletes)."""
    db.session.add(SiteSettings(**_settings_data()))
    db.session.add(AboutContent(**_about_data()))
    for entry in _timeline_data():
        db.session.add(TimelineEntry(**entry))
    for project in _project_data():
        db.session.add(Project(**project))


def seed_if_empty():
    """Populate baseline content when the database has no site settings yet."""
    if SiteSettings.query.first() is not None:
        return
    _insert_all()
    db.session.commit()


def refresh_content():
    """Replace seeded content on an existing database.

    Deletes and re-inserts SiteSettings, AboutContent, TimelineEntry, and
    Project rows from the current seed data. Uploaded photos are untouched;
    the CV PDF reference and project thumbnails (matched by title) carry over.
    """
    existing_settings = SiteSettings.query.first()
    cv_pdf = existing_settings.cv_pdf_filename if existing_settings else None
    thumbnails = {
        p.title: p.thumbnail_filename
        for p in Project.query.all()
        if p.thumbnail_filename
    }

    for model in (SiteSettings, AboutContent, TimelineEntry, Project):
        model.query.delete()

    _insert_all()
    db.session.flush()

    settings = SiteSettings.query.first()
    settings.cv_pdf_filename = cv_pdf
    for project in Project.query.all():
        if project.title in thumbnails:
            project.thumbnail_filename = thumbnails[project.title]

    db.session.commit()
