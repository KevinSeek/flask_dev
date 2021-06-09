from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

# Instantiate Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'                                         # Set the endpoint for the login page


def create_app(config_name):
    """Application Factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Call the inti_app() method on the extension that were created eariler
    # completes their initialization
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # main blueprint registration
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Auth blueprint registration
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app