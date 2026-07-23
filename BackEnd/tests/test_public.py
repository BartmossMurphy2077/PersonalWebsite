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


def test_layout_carries_cynosure_facility_chrome(client):
    """Facility hooks are always server-rendered; blackwall CSS reveals them."""
    response = client.get("/")
    body = response.data
    assert b'id="cyno-status"' in body          # containment status bar
    assert b'id="cyno-lore-flash"' in body      # background lore ticker
    assert b'id="cyno-breach"' in body          # breach percentage tick
    assert b"site-c" in body                    # facility nav label
    assert b"personnel" in body
    assert b"dataspikes" in body
    assert b"clearance" in body
    assert b"img/samurai.png" in body           # footer Samurai stamp


def test_non_home_pages_nudge_back_to_core_to_reseal(client):
    about = client.get("/about").data
    assert b"RETURN TO SITE-C CORE TO RESEAL" in about
    # Home instead reports its terminal is the door out.
    home = client.get("/").data
    assert b"AWAITING RESEAL" in home
    assert b"RETURN TO SITE-C CORE TO RESEAL" not in home


def test_home_carries_site_c_dossier_and_militech_stamp(client):
    body = client.get("/").data
    assert b'id="cyno-dossier"' in body
    assert b"SITE-C PERSONNEL DOSSIER" in body
    assert b"img/militech.webp" in body
    assert b'id="terminal"' in body  # reseal/icebreak command surface


def test_about_carries_netwatch_dossier_stamp(client):
    body = client.get("/about").data
    assert b'id="cyno-netwatch-dossier"' in body
    assert b"img/netwatch.png" in body


def test_projects_page_has_core_dump_and_masonry_hooks(client):
    body = client.get("/projects").data
    assert b'id="cyno-core-dump"' in body       # featured terminal dump
    assert b"img/arasaka.svg" in body           # rival watermark
    assert b'class="project-card is-featured"' in body  # masonry featured span
    assert b"cyno-node-tag" in body             # node cluster labels
    # Real content is still underneath the framing.
    assert b"PromptInjectionTester" in body


def test_facility_stamps_are_served_from_static(client):
    for path in (
        "/static/img/militech.webp",
        "/static/img/netwatch.png",
        "/static/img/arasaka.svg",
        "/static/img/samurai.png",
    ):
        assert client.get(path).status_code == 200


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
