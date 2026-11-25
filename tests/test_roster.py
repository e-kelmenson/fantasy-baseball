import pytest
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Player, RosterEntry, Team, User


def test_roster_entry_connects_user_to_player(app):
    with app.app_context():
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
    with app.app_context():
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



def test_players_page_shows_database_players_and_add_form(client, app):
    with app.app_context():
        team = Team(name="Test Team")
        player = Player(
            name="Sample Hitter",
            position="OF",
            team=team,
        )
        db.session.add(player)
        db.session.commit()

    response = client.get("/players")

    assert response.status_code == 200
    assert b"Sample Hitter" in response.data
    assert b"Test Team" in response.data
    assert b"Add to roster" in response.data
    assert b"/roster/add/" in response.data


def test_roster_page_requires_login(client):
    response = client.get("/roster")

    assert response.status_code == 302
    assert "/login" in response.location


def test_roster_page_shows_added_players(client, app):
    client.post(
        "/sign-up",
        data={
            "email": "roster-page-test@example.com",
            "firstName": "Roster Tester",
            "password1": "practice-password",
            "password2": "practice-password",
        },
    )

    with app.app_context():
        team = Team(name="Roster Page Test Team")
        player = Player(
            name="Roster Page Test Player",
            position="OF",
            team=team,
        )
        db.session.add(player)
        db.session.commit()
        player_id = player.id

    add_response = client.post(f"/roster/add/{player_id}")
    assert add_response.status_code == 302

    response = client.get("/roster")

    assert response.status_code == 200
    assert b"Roster Page Test Player" in response.data
    assert b"Roster Page Test Team" in response.data


def test_roster_page_roster_not_viewable_by_other_users(client, app):
    client.post(
        "/sign-up",
        data={
                "email": "roster-page-test@example.com",
                "firstName": "Roster Tester",
                "password1": "practice-password",
                "password2": "practice-password", 
        },
    )

    with app.app_context():
        team = Team(name="Roster Page Test Team")
        player = Player(
            name="Roster Page Test Player",
            position="OF",
            team=team,
        )
        db.session.add(player)
        db.session.commit()
        player_id = player.id

    add_response = client.post(f"/roster/add/{player_id}")
    assert add_response.status_code == 302

    second_client = app.test_client()
    second_client.post(
            "/sign-up",
            data={
                    "email": "roster-page-test2@example.com",
                    "firstName": "Roster Tester 2",
                    "password1": "practice-password2",
                    "password2": "practice-password2", 
            },
        )
    
    response = second_client.get("/roster")

    assert response.status_code == 200
    assert b"Roster Page Test Player" not in response.data


def test_roster_page_removing_player_requires_login(client):
    response = client.post("/roster/remove/1")

    assert response.status_code == 302
    assert "/login" in response.location


def test_roster_page_logged_in_user_can_remove_their_own_player(client, app):
    client.post(
            "/sign-up",
            data={
                    "email": "roster-page-test@example.com",
                    "firstName": "Roster Tester",
                    "password1": "practice-password",
                    "password2": "practice-password", 
            },
        )
    
    with app.app_context():
        team = Team(name="Roster Page Test Team")
        player = Player(
            name="Roster Page Test Player",
            position="OF",
            team=team,
        )
        db.session.add(player)
        db.session.commit()
        player_id = player.id

    client.post(f"/roster/add/{player_id}")

    with app.app_context():
        user = User.query.filter_by(email="roster-page-test@example.com").first()
        entry = RosterEntry.query.filter_by(
            user_id=user.id,
            player_id=player_id,
        ).first()
        entry_id = entry.id

    remove_response = client.post(f"/roster/remove/{entry_id}")
    assert remove_response.status_code == 302

    roster_response = client.get("/roster")
    assert roster_response.status_code == 200
    assert b"Roster Page Test Player" not in roster_response.data


def test_roster_page_user_cannot_remove_another_users_player(client, app):
    client.post(
                "/sign-up",
                data={
                        "email": "roster-page-test@example.com",
                        "firstName": "Roster Tester",
                        "password1": "practice-password",
                        "password2": "practice-password", 
                },
            )
        
    with app.app_context():
        team = Team(name="Roster Page Test Team")
        player = Player(
            name="Roster Page Test Player",
            position="OF",
            team=team,
        )
        db.session.add(player)
        db.session.commit()
        player_id = player.id

    client.post(f"/roster/add/{player_id}")

    with app.app_context():
        first_user = User.query.filter_by(
            email="roster-page-test@example.com"
        ).first()
        entry = RosterEntry.query.filter_by(
            user_id=first_user.id,
            player_id=player_id,
        ).first()
        entry_id = entry.id

    second_client = app.test_client()
    second_client.post(
            "/sign-up",
            data={
                    "email": "roster-page-test2@example.com",
                    "firstName": "Roster Tester 2",
                    "password1": "practice-password2",
                    "password2": "practice-password2", 
            },
        )

    response = second_client.post(f"/roster/remove/{entry_id}")
  
    assert response.status_code == 404

    first_user_roster = client.get("/roster")
    assert b"Roster Page Test Player" in first_user_roster.data