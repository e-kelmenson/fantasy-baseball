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