from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate



db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yoursecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Register Blueprints
    from .routes.teams import teams_bp
    app.register_blueprint(teams_bp)

    from .routes.players import players_bp
    app.register_blueprint(players_bp)

    from .routes.roster import roster_bp
    app.register_blueprint(roster_bp)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.games import games_bp
    app.register_blueprint(games_bp)

    @app.route("/")
    def home():
        return render_template("home.html")  # Make a home.html template

    return app