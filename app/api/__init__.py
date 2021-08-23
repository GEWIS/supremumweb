from flask import Blueprint

api_bp = Blueprint(
    'api', __name__,
    static_folder=None,
    template_folder=None
)

from . import routes