from flask import Blueprint

supremum_bp = Blueprint(
    'supremum', __name__, 
    static_folder='static', 
    template_folder='templates'
)

from . import routes
