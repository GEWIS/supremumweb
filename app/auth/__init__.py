from flask import Blueprint

auth_bp = Blueprint(
    "auth", __name__,
    static_folder=None,
    template_folder=None
)

from . import routes