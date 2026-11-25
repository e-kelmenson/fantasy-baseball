from flask import Blueprint, render_template

from ..models import Player

players_bp = Blueprint('players', __name__)

@players_bp.route('/players')
def show_players():
    players = Player.query.order_by(Player.name).all()
    return render_template("players.html", players=players)