from flask import Blueprint, abort, flash, redirect, url_for
from flask_login import current_user, login_required

from .. import db
from ..models import Player, RosterEntry


roster_bp = Blueprint("roster", __name__)


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