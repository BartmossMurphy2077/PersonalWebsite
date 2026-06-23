```
 ██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗ █████╗ ██╗
 ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║
 ██████╔╝█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║███████║██║
 ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║██╔══██║██║
 ██║     ███████╗██║  ██║███████║╚██████╔╝██║ ╚████║██║  ██║███████╗
 ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
        ██╗  ██╗ ██████╗ ████████╗██╗   ██╗ ██████╗
        ██║  ██║██╔═══██╗╚══██╔══╝██║   ██║██╔════╝
        ███████║██║   ██║   ██║   ██║   ██║██║  ███╗
        ██╔══██║██║   ██║   ██║   ██║   ██║██║   ██║
        ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╔╝
        ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝

              // NETRUNNER INTERFACE v2.077 — ONLINE
              // WAKE UP, SAMURAI. WE HAVE A PORTFOLIO TO BUILD.
```

# PersonalWebsite

> *A personal portfolio rigged like a netrunner's deck — Flask + SQLite under the hood,
> terminal widgets on the surface, and something lurking behind the ICE.*

Public pages (Home, About, Projects, CV) are content-managed through a password-protected
`/admin` dashboard. No code edits needed to update your story.

---

## Features

| Surface | What it does |
|---------|----------------|
| **Public site** | Split hero, typewriter subtitles, interactive terminal, project grid, CV timeline + PDF, photo gallery, terminal-boot page transitions |
| **Themes** | Light (recruiter mode), Dark (dev terminal), and a hidden **Netrunner** theme behind the ICE |
| **Admin** (`/admin`) | CRUD for settings, photos, CV/experience, projects, about copy. Single-password login |

### Theme system

```
LIGHT ........ recruiter-safe, clean sans-serif
DARK  ........ dev terminal aesthetic, monospace headings
NETRUNNER .... cyan + magenta phosphor glow, full monospace, scanlines
```

Toggle **light ↔ dark** with the sun/moon button in the nav.

The **Netrunner** theme is not in the toggle. You have to breach the ICE yourself.

---

## // EASTER EGG — ICE BREAK PROTOCOL

On the **home page terminal**, type:

```bash
theme icebreak
```

If your ICE holds, you'll see something like:

```
BREACHING ICE...
ARASAKA DAEMON.SYS .............. NEUTRALIZED
BLACKWALL HANDSHAKE ............. OK
FLATLINE PROTOCOL ............... BYPASSED
> Rache Bartmoss and Spider Murphy was here
THEME PACK DECRYPTED: PHOSPHOR_NET
```

Then the site flatlines for a split second and boots into **Netrunner mode**.

Other terminal commands:

```bash
theme light      # back to recruiter mode
theme dark       # dev terminal mode
help             # hints that some themes are hidden (doesn't spoil the command)
```

> *"Some themes are hidden." — that's your only hint. Good luck, choom.*

---

## Architecture

```
┌──────────┐     ┌─────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────────┐
│ Browser  │────▶│  nginx  │────▶│ gunicorn │────▶│  Flask app  │────▶│ SQLite +     │
│          │     │ web tier│     │          │     │  (monolith) │     │ uploads/     │
└──────────┘     └─────────┘     └──────────┘     └─────────────┘     └──────────────┘
```

Flask serves public HTML, admin dashboard, static assets, and uploaded media.
SQLite stores content; files live on disk.

Local dev runs Flask directly. Docker puts nginx in front (see below).

---

## Running locally (no Docker)

```bash
cd BackEnd
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

From the **repository root**, create your `.env`:

```bash
copy .env.example .env         # Windows
cp .env.example .env           # macOS/Linux
```

Set `ADMIN_PASSWORD` and `SECRET_KEY`. Same `.env` for local and Docker.

```bash
cd BackEnd
python backend.py
```

| Endpoint | URL |
|----------|-----|
| Site | http://127.0.0.1:5000 |
| Admin | http://127.0.0.1:5000/admin/login |

Database seeds on first run.

---

## Running with Docker

From the **repository root**:

```bash
cp .env.example .env           # skip if you already have one
docker compose -f infrastructure/docker-compose.yml up --build
```

| Endpoint | URL |
|----------|-----|
| Site | http://localhost:8080 |
| Admin | http://localhost:8080/admin/login |

Data persists in the `portfolio-data` volume. Nuke everything and start fresh:

```bash
docker compose -f infrastructure/docker-compose.yml down -v
```

---

## Running tests

```bash
cd BackEnd
python -m pytest
```

21 HTTP-seam tests. Isolated temp DB per run — your live data stays untouched.

---

## Project layout

```
.env.example              # env template → copy to .env at repo root
BackEnd/
  app/
    __init__.py           # app factory + 404 handler
    config.py             # env-driven config
    models.py             # SQLite schema
    seed.py               # first-run content (LinkedIn/GitHub sourced)
    auth.py               # admin session login
    public.py             # Home, About, Projects, CV
    admin.py              # dashboard CRUD
    uploads.py            # file upload helpers
    templates/            # Jinja (public/ + admin/ + 404)
    static/
      css/main.css        # 3-theme token system (light/dark/netrunner)
      js/
        theme.js          # theme toggle + localStorage
        home.js           # terminal widget + icebreak sequence
        reveal.js         # scroll-reveal animations
        transitions.js    # terminal-boot page transitions
  tests/
  backend.py              # dev entry point
  requirements.txt
infrastructure/
  docker-compose.yml
  backend.Dockerfile
  nginx.Dockerfile
  nginx/default.conf
```

---

## Security follow-ups (before going public)

```
[ ] CSRF protection on admin forms (Flask-WTF)
[ ] Enforce non-default ADMIN_PASSWORD (no changeme fallback)
[ ] TLS/HTTPS at nginx (443 + cert)
```

---

```
// END OF TRANSMISSION
// Rache Bartmoss and Spider Murphy was here
// STAY CHROME, CHOOM.
```
