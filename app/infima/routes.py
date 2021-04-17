from flask import render_template, jsonify
from . import infima_bp


@infima_bp.route('/')
def infima_overview():
    return "This is a temporary infima overview"
