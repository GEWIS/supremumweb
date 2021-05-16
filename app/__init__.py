from flask import Flask

from app import config
from app.database import db
from app.home import home_bp
from app.infima import infima_bp
from app.supremum import supremum_bp


def create_app(config=config.base_config):
    app = Flask(__name__, static_folder=None, template_folder=None)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(infima_bp, url_prefix='/infima')
    app.register_blueprint(supremum_bp, url_prefix='/supremum')
