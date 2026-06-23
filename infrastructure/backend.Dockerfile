# Backend image: the Flask portfolio CMS served by gunicorn.
# Build context is the repository root (see docker-compose.yml).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies first so layer caching survives source changes.
COPY BackEnd/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn==23.0.0

# Application code.
COPY BackEnd/ /app/

# Data directory for the SQLite database and uploads (mounted as a volume).
RUN mkdir -p /data/uploads

EXPOSE 8000

# backend.py exposes `app = create_app()`.
# --preload loads the app once before forking workers, avoiding a race when
# both workers call db.create_all() on startup.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--preload", "--timeout", "60", "backend:app"]
