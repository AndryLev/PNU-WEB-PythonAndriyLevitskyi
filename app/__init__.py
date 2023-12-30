from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import config

bcrypt = Bcrypt()
migrate = Migrate()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="default"):
    if not config_name in config:
        config_name = "default"
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():

        from .auth import auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .portfolio import portfolio_blueprint
        app.register_blueprint(portfolio_blueprint)

        app.route('/')(lambda: redirect(url_for('portfolio.home')))

        from .todo import todo_blueprint
        app.register_blueprint(todo_blueprint)

        from .feedback import feedback_blueprint
        app.register_blueprint(feedback_blueprint)

        from .api import api_blueprint
        app.register_blueprint(api_blueprint)

        from .post import post_blueprint
        app.register_blueprint(post_blueprint)
    return app

