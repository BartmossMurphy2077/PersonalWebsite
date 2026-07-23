"""Behaviour tests for the public-facing pages."""

import io


def test_home_shows_seeded_name(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hugo Kotuc" in response.data


def test_home_has_project_and_cv_calls_to_action(client):
    response = client.get("/")
    body = response.data
    assert b"View Projects" in body
    # No CV PDF seeded, so the CTA falls back to the CV page link.
    assert b"/projects" in body
    assert b"/cv" in body


def test_about_page_renders(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"about" in response.data.lower()


def test_projects_page_lists_seeded_project(client):
    response = client.get("/projects")
    assert response.status_code == 200
    assert b"Personal Website CMS" in response.data


def test_projects_page_lists_curated_github_projects(client):
    response = client.get("/projects")
    body = response.data
    assert b"PromptInjectionTester" in body
    assert b"Slang-Aware Sentiment Analysis" in body
    assert b"GPT Challenge" in body
    assert b"Expense Management System" in body
    assert b"Well-Being Visualisation" in body


def test_layout_allowlists_blackwall_theme(client):
    """The pre-paint script accepts blackwall and no longer lists netrunner."""
    response = client.get("/")
    assert b'["light", "dark", "blackwall"]' in response.data
    assert b'["light", "dark", "netrunner"]' not in response.data


def test_layout_mounts_blackwall_canvas(client):
    response = client.get("/")
    assert b'id="blackwall-canvas"' in response.data


def test_footer_has_ice_glyph_breadcrumb(client):
    response = client.get("/about")
    assert b'class="ice-glyph"' in response.data


def test_refresh_content_replaces_stale_copy_but_keeps_cv_pdf(app, client):
    from app.extensions import db
    from app.models import SiteSettings
    from app.seed import refresh_content

    with app.app_context():
        settings = SiteSettings.query.first()
        settings.tagline = "stale tagline"
        settings.cv_pdf_filename = "cv.pdf"
        db.session.commit()

        refresh_content()

        refreshed = SiteSettings.query.first()
        assert refreshed.tagline != "stale tagline"
        assert refreshed.cv_pdf_filename == "cv.pdf"

    # The refreshed copy is what public pages serve.
    response = client.get("/")
    assert b"stale tagline" not in response.data
    assert b"Hugo Kotuc" in response.data


def test_cv_page_lists_timeline_entry(client):
    response = client.get("/cv")
    assert response.status_code == 200
    assert b"IE University" in response.data


def test_cv_download_404_when_no_pdf(client):
    response = client.get("/cv/download")
    assert response.status_code == 404


def test_unknown_route_renders_custom_404(client):
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404
    assert b"command not found" in response.data
    assert b"theme-toggle" in response.data  # full themed layout rendered


def test_uploaded_image_is_served(auth_client):
    """An image uploaded via admin is retrievable through the uploads route."""
    data = {
        "alt_text": "test",
        "photo": (io.BytesIO(b"fake-image-bytes"), "me.png"),
    }
    auth_client.post(
        "/admin/photos", data=data, content_type="multipart/form-data"
    )

    listing = auth_client.get("/admin/photos")
    assert b"/uploads/" in listing.data

    # Pull the served filename out of the admin listing and fetch it.
    marker = b"/uploads/"
    start = listing.data.find(marker)
    end = listing.data.find(b'"', start)
    url = listing.data[start:end].decode()
    served = auth_client.get(url)
    assert served.status_code == 200
    assert served.data == b"fake-image-bytes"
