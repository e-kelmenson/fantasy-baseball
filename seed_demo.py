from app import create_app, db
from app.models import Player, Team


app = create_app()

with app.app_context():
    team = Team.query.filter_by(name="Demo City").first()

    if team is None:
        team = Team(name="Demo City")
        db.session.add(team)
        db.session.flush()

    sample_players = [
        ("Casey Example", "OF"),
        ("Jordan Sample", "SP"),
        ("Riley Demo", "SS"),
    ]

    added_count = 0

    for name, position in sample_players:
        existing_player = Player.query.filter_by(
            name=name,
            team_id=team.id,
        ).first()

        if existing_player is None:
            player = Player(
                name=name,
                position=position,
                team=team,
            )
            db.session.add(player)
            added_count += 1

    db.session.commit()
    print(f"Added {added_count} demo players.")