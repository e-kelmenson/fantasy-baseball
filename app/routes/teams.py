from flask import Blueprint, render_template

teams_bp = Blueprint('teams', __name__)

@teams_bp.route("/teams")
def show_teams():
    # TODO: Replace dummy data with data retrieved from MLB API
    sample_teams = ["Yankees", "Dodgers", "Blue Jays"]
    return render_template("teams.html", teams=sample_teams)