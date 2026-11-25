from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .. import db
from ..models import Player, RosterEntry


roster_bp = Blueprint("roster", __name__)


@roster_bp.route("/roster")
@login_required
def show_roster():
    roster_entries = (
        RosterEntry.query
        .filter_by(user_id=current_user.id)
        .order_by(RosterEntry.id)
        .all()
    )

    return render_template("roster.html", roster_entries=roster_entries)


@roster_bp.route("/roster/add/<int:player_id>", methods=["POST"])
@login_required
def add_player(player_id):
    player = db.session.get(Player, player_id)

    if player is None:
        abort(404)

    existing_entry = RosterEntry.query.filter_by(
        user_id=current_user.id,
        player_id=player.id,
    ).first()

    if existing_entry is not None:
        flash("That player is already on your roster.", category="error")
    else:
        entry = RosterEntry(
            user_id=current_user.id,
            player_id=player.id,
        )
        db.session.add(entry)
        db.session.commit()
        flash("Player added to your roster.", category="success")

    return redirect(url_for("players.show_players"))


@roster_bp.route("/roster/remove/<int:entry_id>", methods=["POST"])
@login_required
def remove_player(entry_id):
    entry = RosterEntry.query.filter_by(
        id = entry_id,
        user_id = current_user.id,
    ).first_or_404()

    db.session.delete(entry)
    db.session.commit()
    flash("Player removed from your roster.", category="success")

    return redirect(url_for("roster.show_roster"))