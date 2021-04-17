from flask import render_template, jsonify
from . import home_bp as home


@home.route('/')
def landing_page():
    return "This is a temporary home"
