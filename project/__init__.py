import os
from . import config
from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from .models import db, User
from flask_login import LoginManager
from .auth_app import auth as auth_blueprint
from .main_app import main as main_blueprint

def create_app(database_url=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="33e08edb07e6fa05800d8fc2188d76d5",
        SQLALCHEMY_DATABASE_URI=config.SQLA_DB_URI,
        UPLOAD_FOLDER=config.UPLOAD_DIR if not database_url else database_url
    )

    db.init_app(app)
    migrate = Migrate(app, db=db)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    app.register_blueprint(auth_blueprint)

    app.register_blueprint(main_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app