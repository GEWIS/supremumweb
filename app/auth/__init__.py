from flask import Blueprint

auth_bp = Blueprint(
    "auth", __name__, 
    static_folder='static',
    template_folder='templates'
)

from . import routes