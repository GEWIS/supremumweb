from flask import Flask

from app.home import home_bp
from app.infima import infima_bp
from app.supremum import supremum_bp


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(infima_bp, url_prefix='/infima')
    app.register_blueprint(supremum_bp, url_prefix='/supremum')
