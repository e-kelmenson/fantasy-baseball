from sqlalchemy import UniqueConstraint
from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)

    roster_entries = db.relationship(
        "RosterEntry",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    players = db.relationship("Player", back_populates="team")


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(10), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    team = db.relationship("Team", back_populates="players")
    roster_entries = db.relationship(
        "RosterEntry",
        back_populates="player",
        cascade="all, delete-orphan",
    )



class RosterEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)

    user = db.relationship("User", back_populates="roster_entries")
    player = db.relationship("Player", back_populates="roster_entries")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "player_id",
            name="unique_user_player_roster_entry",
        ),
    )
