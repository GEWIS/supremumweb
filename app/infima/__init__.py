from flask import Blueprint

infima_bp = Blueprint(
    'infima', __name__,
    static_folder='static',
    template_folder='templates'
)

from . import routes
