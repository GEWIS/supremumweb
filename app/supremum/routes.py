from flask import render_template, jsonify
from . import supremum_bp as supremum


@supremum.route('')
def supremum_overview():
    return "This is the temporary supremum archive"
