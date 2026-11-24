from flask import Blueprint, render_template

games_bp = Blueprint('games', __name__)

@games_bp.route("/games")
def show_games():
    # TODO: Replace dummy data with data retrieved from MLB API
    sample_games = ["Yankees vs. Mets", "Dodgers vs. Padres", "Blue Jays vs. Orioles"]
    return render_template("games.html", games=sample_games)