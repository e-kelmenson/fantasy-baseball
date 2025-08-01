from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'one tree apple window porcupine iceberg queen'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.instance_path, DB_NAME)}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    create_database(app)

    return app


def create_database(app):
    if not path.exists(path.join(app.instance_path, DB_NAME)):
        with app.app_context():
            db.create_all()
            print('Created Database!')
