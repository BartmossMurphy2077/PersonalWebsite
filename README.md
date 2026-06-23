# PersonalWebsite

A personal portfolio site with a private admin dashboard (CMS), built with Flask
+ SQLite. Public pages (Home, About, Projects, CV) are content-managed through a
password-protected `/admin` dashboard — no code edits needed to update content.

## Features

- **Public site**: split hero with photo + interactive terminal widget and
  typewriter subtitles, projects grid, CV timeline with PDF download, about page
  with photo gallery, terminal-boot page transitions.
- **Admin dashboard** (`/admin`): manage site settings, photos, CV/experience
  timeline, projects, and about-page copy. Single-password login.

## Architecture

The Flask app is a self-contained monolith: it serves the public HTML pages, the
admin dashboard, the static assets, and uploaded media. SQLite stores all
content; uploads live on disk.

```
Browser ──▶ nginx (web tier) ──▶ gunicorn ──▶ Flask app ──▶ SQLite + uploads
```

In local development you run the Flask dev server directly. In Docker, nginx sits
in front of gunicorn (see [Running with Docker](#running-with-docker)).

## Running locally (no Docker)

1. Go to the `BackEnd` directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. From the repository root, create your `.env` from the template:
   ```bash
   copy .env.example .env       # Windows
   cp .env.example .env         # macOS/Linux
   ```
   Edit `.env` and set `ADMIN_PASSWORD` and `SECRET_KEY`. The same root `.env`
   is used by both local runs and Docker.
5. Back in `BackEnd`, run the app:
   ```bash
   python backend.py
   ```
6. Open http://127.0.0.1:5000 for the site, and http://127.0.0.1:5000/admin to
   log in and manage content. The database is seeded with starter content on
   first run.

## Running with Docker

All container definitions live in the `infrastructure/` directory, but commands
are run from the repository root so they share the same root `.env`.

1. From the repository root, create your environment file (skip if you already
   made `.env` for local runs):
   ```bash
   cp .env.example .env         # then edit SECRET_KEY and ADMIN_PASSWORD
   ```
2. Build and start the stack:
   ```bash
   docker compose -f infrastructure/docker-compose.yml up --build
   ```
3. Open http://localhost:8080

The SQLite database and uploaded media are stored in the named `portfolio-data`
volume, so they survive container restarts and rebuilds. To wipe all content and
start fresh:

```bash
docker compose -f infrastructure/docker-compose.yml down -v
```

## Running tests

From the `BackEnd` directory:

```bash
python -m pytest
```

Tests exercise the app through the HTTP layer using Flask's test client against
an isolated temporary database and uploads directory.

## Project layout

```
.env.example         # single env template (copy to .env at repo root)
BackEnd/
  app/
    __init__.py      # application factory
    config.py        # configuration (env-driven)
    extensions.py    # SQLAlchemy instance
    models.py        # database models
    seed.py          # first-run seed data
    auth.py          # admin login/logout + login_required
    public.py        # public page routes
    admin.py         # admin CRUD routes
    uploads.py       # file upload helpers
    templates/       # Jinja templates (public/ and admin/)
    static/          # CSS + JS (terminal widget, transitions)
  tests/             # pytest HTTP-seam tests
  backend.py         # dev entry point
  requirements.txt
infrastructure/
  docker-compose.yml # nginx + backend services + data volume
  backend.Dockerfile # gunicorn-served Flask app
  nginx.Dockerfile   # nginx web tier
  nginx/default.conf # reverse-proxy config
```

## Notes

- Local development only for now; production deployment also needs the security
  hardening below.
- The SQLite database, uploaded media, and `.env` files are gitignored.

### Security follow-ups before going public

- **CSRF protection** on admin forms (e.g. Flask-WTF) — not yet added.
- **Enforced non-default admin password** — currently falls back to `changeme`
  for local convenience if `ADMIN_PASSWORD` is unset.
- **TLS/HTTPS** termination at nginx (add a certificate + `443` server block).
