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


def test_cv_page_lists_timeline_entry(client):
    response = client.get("/cv")
    assert response.status_code == 200
    assert b"IE University" in response.data


def test_cv_download_404_when_no_pdf(client):
    response = client.get("/cv/download")
    assert response.status_code == 404


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
