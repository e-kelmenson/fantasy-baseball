from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY is missing. Add it to the local .env files."
        )
    app.config['SECRET_KEY'] = secret_key

    # Use DATABASE_URL from environment, otherwise fallback to SQLite
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Required fix for SQLAlchemy with Postgres URI from Heroku-style env
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        DB_NAME = "database.db"
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, DB_NAME)}'
        os.makedirs(app.instance_path, exist_ok=True)  # ensures instance dir exists

    db.init_app(app)

    # Import views, auth routes
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models and create tables
    from .models import User, Note
    with app.app_context():
        db.create_all()
        print("Database tables created!")

    # Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
