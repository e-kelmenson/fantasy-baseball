import pytest
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Player, RosterEntry, Team, User


def test_roster_entry_connects_user_to_player(app):
    user = User(
        email="learner@example.com",
        password="test-password",
        first_name="Learner",
    )
    team = Team(name="New York Yankees")
    player = Player(
        name="Sample Player",
        position="OF",
        team=team,
    )
    roster_entry = RosterEntry(user=user, player=player)

    db.session.add(roster_entry)
    db.session.commit()

    assert roster_entry in user.roster_entries
    assert roster_entry in player.roster_entries
    assert roster_entry.player.team.name == "New York Yankees"


def test_user_cannot_add_same_player_twice(app):
    user = User(
        email="duplicate-test@example.com",
        password="test-password",
        first_name="Tester",
    )
    team = Team(name="New York Yankees")
    player = Player(
        name="Sample Player",
        position="OF",
        team=team,
    )

    db.session.add(RosterEntry(user=user, player=player))
    db.session.commit()

    duplicate_entry = RosterEntry(user=user, player=player)
    db.session.add(duplicate_entry)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


def test_add_player_requires_login(client):
    response = client.post("/roster/add/1")

    assert response.status_code == 302
    assert "/login" in response.location


def test_logged_in_user_can_add_player_once(client, app):
    signup_response = client.post(
        "/sign-up",
        data={
            "email": "roster-test@example.com",
            "firstName": "Roster Tester",
            "password1": "practice-password",
            "password2": "practice-password",
        },
    )
    assert signup_response.status_code == 302

    with app.app_context():
        team = Team(name="New York Yankees")
        player = Player(
            name="Sample Player",
            position="OF",
            team=team,
        )
        db.session.add(player)
        db.session.commit()
        player_id = player.id

    first_response = client.post(f"/roster/add/{player_id}")
    second_response = client.post(f"/roster/add/{player_id}")

    assert first_response.status_code == 302
    assert second_response.status_code == 302

    with app.app_context():
        user = User.query.filter_by(email="roster-test@example.com").first()
        entries = RosterEntry.query.filter_by(
            user_id=user.id,
            player_id=player_id,
        ).all()

        assert len(entries) == 1
