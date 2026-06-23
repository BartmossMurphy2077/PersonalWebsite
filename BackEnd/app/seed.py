"""Seed the database with Hugo's real content (sourced from his LinkedIn and
GitHub) so the CMS is never empty on first run."""

from .extensions import db
from .models import AboutContent, Project, SiteSettings, TimelineEntry


def seed_if_empty():
    """Populate baseline content when the database has no site settings yet."""
    if SiteSettings.query.first() is not None:
        return

    settings = SiteSettings(
        name="Hugo Kotuc",
        tagline="Computer Science & AI Student · AI Research Intern",
        hero_bio=(
            "Computer Science & AI student at IE University and research intern "
            "at the Kempelen Institute of Intelligent Technologies (KInIT). I "
            "build AI systems - lately Retrieval-Augmented Generation and "
            "agentic tooling - and like turning messy problems into clean, "
            "working software."
        ),
        github_url="https://github.com/BartmossMurphy2077",
        linkedin_url="https://www.linkedin.com/in/hugo-kotuc-b0baa8311/",
        subtitle_lines=[
            "Researching AI at KInIT",
            "CS & AI @ IE University",
            "RAG & prompt-injection tinkerer",
            "2nd place @ Talent Arena hackathon",
            "Probably debugging something",
        ],
        terminal_responses={
            "whoami": "Hugo Kotuc - CS & AI student @ IE University, AI research intern @ KInIT",
            "skills": "Python, Java, C, AI Agents, RAG, Docker, React, CI/CD, Git",
            "projects": "PromptInjectionTester, this site, CI/CD exercises - see /projects",
            "languages": "Slovak (native), English (native), Spanish (working), Mandarin (basic)",
            "help": "Available commands: whoami, skills, projects, languages, help",
        },
    )
    db.session.add(settings)

    about = AboutContent(
        long_bio=(
            "I'm Hugo, a Computer Science & Artificial Intelligence student at "
            "IE University in Segovia, Spain, originally from Bratislava, "
            "Slovakia.\n\n"
            "I'm currently a research intern at the Kempelen Institute of "
            "Intelligent Technologies (KInIT), a nonprofit AI research "
            "institute. Previously I interned at Vacuumlabs, where I researched "
            "Retrieval-Augmented Generation (RAG), cleaned up CRM data, and "
            "helped improve their AI academy.\n\n"
            "I like building things and competing - my team recently placed 2nd "
            "at a hackathon and represented at Talent Arena and MWC in "
            "Barcelona."
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
    db.session.add(about)

    # --- Experience & education timeline (most recent first) ---
    db.session.add(
        TimelineEntry(
            title="Research Intern",
            organization="Kempelen Institute of Intelligent Technologies (KInIT)",
            start_date="Aug 2025",
            end_date="",
            bullets=[
                "AI research at a nonprofit intelligent-technologies institute",
                "Working on Retrieval-Augmented Generation and agentic tooling",
            ],
            display_order=0,
        )
    )
    db.session.add(
        TimelineEntry(
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
        )
    )
    db.session.add(
        TimelineEntry(
            title="BSc Computer Science & Artificial Intelligence",
            organization="IE University, Segovia",
            start_date="2023",
            end_date="2027",
            bullets=[
                "Computer Science and Artificial Intelligence degree",
                "Active in hackathons and the campus tech community",
            ],
            display_order=2,
        )
    )
    db.session.add(
        TimelineEntry(
            title="IB Diploma (IBDP) & IGCSE",
            organization="British International School of Bratislava (Nord Anglia)",
            start_date="2016",
            end_date="2023",
            bullets=[
                "IB Computer Science HL, Economics HL, Math HL",
                "Coding club and Eco committee",
            ],
            display_order=3,
        )
    )

    # --- Selected projects (from GitHub) ---
    db.session.add(
        Project(
            title="PromptInjectionTester",
            description=(
                "A tool that feeds datasets of prompt injections to a tester "
                "model; an auditor then classifies each attempt as BREACH or "
                "SAFE - a small harness for evaluating LLM prompt-injection "
                "resistance."
            ),
            tech_tags=["Python", "LLMs", "AI Security"],
            github_url="https://github.com/BartmossMurphy2077/PromptInjectionTester",
            demo_url="",
            is_featured=True,
            display_order=0,
        )
    )
    db.session.add(
        Project(
            title="Personal Website CMS",
            description=(
                "This very site - a Flask + SQLite portfolio with a custom "
                "admin dashboard for managing projects, photos, and CV content, "
                "containerised with Docker."
            ),
            tech_tags=["Python", "Flask", "SQLite", "Docker", "JavaScript"],
            github_url="https://github.com/BartmossMurphy2077/PersonalWebsite",
            demo_url="",
            is_featured=False,
            display_order=1,
        )
    )
    db.session.add(
        Project(
            title="CI Pipeline Exercise",
            description=(
                "A hands-on Continuous Integration exercise using GitHub "
                "Actions - learn by fixing bugs across branches."
            ),
            tech_tags=["GitHub Actions", "CI", "Python"],
            github_url="https://github.com/BartmossMurphy2077/ci_exercise_hugo",
            demo_url="",
            is_featured=False,
            display_order=2,
        )
    )
    db.session.add(
        Project(
            title="CD Pipeline Exercise",
            description=(
                "A hands-on exercise for learning Continuous Deployment (CD) "
                "pipelines with GitHub Actions."
            ),
            tech_tags=["GitHub Actions", "CD", "Python"],
            github_url="https://github.com/BartmossMurphy2077/cd_exercise_hugoK",
            demo_url="",
            is_featured=False,
            display_order=3,
        )
    )

    db.session.commit()
