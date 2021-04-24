from flask import render_template, jsonify, url_for
from . import supremum_bp as supremum


@supremum.route('')
def supremum_overview():
    temp_editions = [
        {
            'title': 'The Wind Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.1'
        },
        {
            'title': 'The Earth Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.0'
        },
        {
            'title': 'The Default Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 52.2'
        },
        {
            'title': 'The Miracle Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 52.1'
        },
        {
            'title': 'The Disaster Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 52.0'
        }
    ]
    return render_template('archive.html', editions=temp_editions)
