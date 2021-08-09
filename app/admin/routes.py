from flask import render_template, url_for
from flask_login import login_required

from app.admin import admin_bp as admin

@admin.route('/')
# @login_required
def index():
    temp_editions = [
        {
            'title': 'The Wind Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.1',
            'id': 4
        },
        {
            'title': 'The Earth Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.0',
            'id': 3
        },
        {
            'title': 'The Default Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 52.2',
            'id': 2
        },
        {
            'title': 'The Miracle Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 52.1',
            'id': 1
        },
        {
            'title': 'The Disaster Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 52.0',
            'id': 0
        }
    ]
    return render_template('index.html', editions=temp_editions), 200

@admin.route('/supremum/edit/<int:sid>')
def edit_supremum(sid: int):
    return "Not yet implemented", 404