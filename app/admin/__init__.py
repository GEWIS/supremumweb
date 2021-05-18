from flask import Blueprint

admin_bp = Blueprint(
    "admin", __name__,
    static_folder='static',
    template_folder='templates'
)

from . import routes