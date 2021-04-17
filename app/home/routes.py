from flask import render_template, jsonify, url_for
from . import home_bp as home


@home.route('/')
def landing_page():
    temp_edition = {
        'title': 'The Earth Edition',
        'img_url' : url_for("home.static", filename="latest_edition.png"),
        'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
        'name': 'Supremum 53.0'
    }
    return render_template('home.html', edition=temp_edition)
