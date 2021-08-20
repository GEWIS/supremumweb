from flask import Flask

from app import config
from app.admin import admin_bp
from app.auth import auth_bp
from app.database import db
from app.extensions import lm
from app.home import home_bp


def create_app(config=config.base_config):
    app = Flask(__name__, static_folder=None, template_folder=None)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    lm.init_app(app)
    lm.login_view = 'auth.login'  # TODO: give this a better spot...


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(home_bp)
