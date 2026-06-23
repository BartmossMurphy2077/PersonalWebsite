"""Behaviour tests for admin auth and content management."""

import io
import re


def test_admin_requires_login(client):
    response = client.get("/admin/settings")
    assert response.status_code == 302
    assert "/admin/login" in response.headers["Location"]


def test_login_with_wrong_password_fails(client):
    response = client.post(
        "/admin/login", data={"password": "nope"}, follow_redirects=True
    )
    assert b"Incorrect password" in response.data


def test_login_with_correct_password_grants_access(client, app):
    client.post("/admin/login", data={"password": app.config["ADMIN_PASSWORD"]})
    response = client.get("/admin/settings")
    assert response.status_code == 200
    assert b"Site Settings" in response.data


def test_login_ignores_external_next_redirect(client, app):
    response = client.post(
        "/admin/login?next=https://evil.example",
        data={"password": app.config["ADMIN_PASSWORD"]},
    )
    assert response.status_code == 302
    location = response.headers["Location"]
    assert "evil.example" not in location
    assert "/admin" in location


def test_logout_blocks_admin_again(auth_client):
    assert auth_client.get("/admin/settings").status_code == 200
    auth_client.post("/admin/logout")
    blocked = auth_client.get("/admin/settings")
    assert blocked.status_code == 302
    assert "/admin/login" in blocked.headers["Location"]


def test_creating_project_appears_on_public_page(auth_client, client):
    auth_client.post(
        "/admin/projects/new",
        data={
            "title": "Neural Doodler",
            "description": "A quirky generative art toy.",
            "tech_tags": "Python, PyTorch",
            "display_order": "0",
        },
    )
    response = client.get("/projects")
    assert b"Neural Doodler" in response.data
    assert b"PyTorch" in response.data


def test_editing_project_updates_public_page(auth_client, client):
    auth_client.post(
        "/admin/projects/new",
        data={"title": "Old Title", "description": "x", "display_order": "99"},
    )
    # The high display_order sorts this project last in the admin listing.
    listing = auth_client.get("/admin/projects").data.decode()
    ids = re.findall(r"/admin/projects/(\d+)/edit", listing)
    assert ids
    project_id = ids[-1]

    auth_client.post(
        f"/admin/projects/{project_id}/edit",
        data={"title": "New Title", "description": "y", "display_order": "99"},
    )
    response = client.get("/projects")
    assert b"New Title" in response.data
    assert b"Old Title" not in response.data


def test_deleting_project_removes_it_from_public_page(auth_client, client):
    auth_client.post(
        "/admin/projects/new",
        data={"title": "Disposable", "description": "x", "display_order": "99"},
    )
    # The high display_order sorts this project last in the admin listing.
    listing = auth_client.get("/admin/projects").data.decode()
    project_id = re.findall(r"/admin/projects/(\d+)/delete", listing)[-1]
    auth_client.post(f"/admin/projects/{project_id}/delete")

    response = client.get("/projects")
    assert b"Disposable" not in response.data


def test_settings_update_changes_home_page(auth_client, client):
    auth_client.post(
        "/admin/settings",
        data={
            "name": "Hugo K",
            "tagline": "Builder",
            "hero_bio": "New bio here.",
            "github_url": "",
            "linkedin_url": "",
            "subtitle_lines": "line one\nline two",
        },
    )
    response = client.get("/")
    assert b"New bio here." in response.data


def test_timeline_entry_creation_shows_on_cv(auth_client, client):
    auth_client.post(
        "/admin/cv/entries",
        data={
            "title": "Intern",
            "organization": "Cool Corp",
            "start_date": "2022",
            "end_date": "2023",
            "bullets": "Did things\nDid other things",
        },
    )
    response = client.get("/cv")
    assert b"Cool Corp" in response.data


def test_cv_pdf_upload_enables_download(auth_client, client):
    auth_client.post(
        "/admin/cv/pdf",
        data={"cv_pdf": (io.BytesIO(b"%PDF-1.4 fake"), "cv.pdf")},
        content_type="multipart/form-data",
    )
    response = client.get("/cv/download")
    assert response.status_code == 200
    assert response.data == b"%PDF-1.4 fake"


def test_about_update_shows_on_about_page(auth_client, client):
    auth_client.post(
        "/admin/about",
        data={"long_bio": "I build things.", "interests": "Chess"},
    )
    response = client.get("/about")
    assert b"I build things." in response.data
    assert b"Chess" in response.data


def test_photo_upload_rejects_non_image(auth_client):
    response = auth_client.post(
        "/admin/photos",
        data={"photo": (io.BytesIO(b"data"), "evil.exe")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert b"Unsupported image type" in response.data
