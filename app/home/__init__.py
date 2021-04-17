from flask import Blueprint

home_bp = Blueprint(
    'home', __name__, 
    static_folder='static', 
    template_folder='templates'
)

from . import routes
