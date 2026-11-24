import pytest
from website import create_app

@pytest.fixture()
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{test_db}")
    monkeypatch.setenv("SECRET_KEY", "test-only-secret-key")

    app = create_app()
    app.config.update(TESTING=True)

    return app.test_client()


def test_signup_logs_user_in_and_shows_notes_page(client):
    response = client.post(
        "/sign-up",
        data={
            "email": "learner@example.com",
            "firstName": "Learner",
            "password1": "practice-password",
            "password2": "practice-password",
        },
        follow_redirects = True,
    )

    assert response.status_code == 200
    assert b"Notes" in response.data
    assert b"Add Note" in response.data


def test_signup_rejects_missing_fields(client):
    response = client.post("/sign-up", data={})
    assert response.status_code == 200
    assert b"Please fill out all fields." in response.data


def test_note_rejects_blank_content(client):
    client.post(
        "/sign-up",
        data={
            "email": "note-test@example.com",
            "firstName": "Note Tester",
            "password1": "practice-password",
            "password2": "practice-password",
        },
    )

    response = client.post("/", data={"note": "    "})

    assert response.status_code == 200
    assert b"Note is too short." in response.data


def test_delete_note_requires_login(client):
    response = client.post("/delete-note", json={"noteId": 1})

    assert response.status_code == 302
    assert "/login" in response.location


def test_delete_note_rejects_malformed_json(client):
    client.post(
        "/sign-up",
        data={
            "email": "delete-test@example.com",
            "firstName": "Delete Tester",
            "password1": "practice-password",
            "password2": "practice-password",
        },
    )

    response = client.post(
        "/delete-note",
        data="not JSON",
        content_type="application/json",
    )

    assert response.status_code == 400