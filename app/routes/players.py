from flask import Blueprint, render_template

players_bp = Blueprint('players', __name__)

@players_bp.route('/players')
def show_players():
    # TODO: Replace dummy data with data retrieved from MLB API
    sample_players = ["Aaron Judge", "Shohei Ohtani", "Bobby Witt Jr."]
    return render_template("players.html", players=sample_players)