from flask import render_template, jsonify, url_for
from . import supremum_bp as supremum


@supremum.route('')
def supremum_overview():
    volumes = {
            53: [
                {
                    'title': 'The Wind Edition',
                    'img_url' : url_for("home.static", filename="latest_edition.png"),
                    'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
                    'name': 'Supremum 53.1',
                    'edition': '1'
                },
                {
                    'title': 'The Earth Edition',
                    'img_url' : url_for("home.static", filename="latest_edition.png"),
                    'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
                    'name': 'Supremum 53.0',
                    'edition': '0'
                },
            ],
            52: [
                {
                    'title': 'The Default Edition',
                    'img_url' : url_for("home.static", filename="latest_edition.png"),
                    'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
                    'name': 'Supremum 52.2',
                    'edition': '2'
                },
                {
                    'title': 'The Miracle Edition',
                    'img_url' : url_for("home.static", filename="latest_edition.png"),
                    'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
                    'name': 'Supremum 52.1',
                    'edition': '1'
                },
                {
                    'title': 'The Disaster Edition',
                    'img_url' : url_for("home.static", filename="latest_edition.png"),
                    'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
                    'name': 'Supremum 52.0',
                    'edition': '0'
                }        
            ]
        }
    return render_template('archive.html', volumes=volumes)
