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

## Getting Started

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
4. Create your `.env` from the template and set a password + secret:
   ```bash
   copy .env.example .env       # Windows
   cp .env.example .env         # macOS/Linux
   ```
   Edit `.env` and set `ADMIN_PASSWORD` and `SECRET_KEY`.
5. Run the app:
   ```bash
   python backend.py
   ```
6. Open http://127.0.0.1:5000 for the site, and http://127.0.0.1:5000/admin to
   log in and manage content. The database is seeded with starter content on
   first run.

## Running tests

From the `BackEnd` directory:

```bash
python -m pytest
```

Tests exercise the app through the HTTP layer using Flask's test client against
an isolated temporary database and uploads directory.

## Project layout

```
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
  .env.example
```

## Notes

- Local development only for now; production deployment (and the security
  hardening that comes with it — CSRF protection, enforced non-default
  password) is a planned follow-up.
- The SQLite database, uploaded media, and `.env` are gitignored.
