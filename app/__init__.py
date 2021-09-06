from flask import Flask

from app import config
from app.admin import admin_bp
from app.api import api_bp
from app.auth import auth_bp
from app.database import db
from app.extensions import cache, cors, lm
from app.home import home_bp
from app.tools import http_code


def create_app(config=config.base_config):
    app = Flask(__name__, static_folder=config.DATA_PATH,
                static_url_path='/data', template_folder=None)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    cors.init_app(app)
    lm.init_app(app)
    lm.login_view = 'auth.login'  # TODO: give this a better spot...


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

def register_error_handlers(app):
    app.register_error_handler(400, http_code)
    app.register_error_handler(401, http_code)
    app.register_error_handler(403, http_code)
    app.register_error_handler(404, http_code)
    app.register_error_handler(409, http_code)
    app.register_error_handler(500, http_code)
