from flask import render_template, url_for, redirect
from flask_login import login_required

from app.admin import admin_bp as admin
from app.admin.forms import SupremumForm

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
    # TODO: retrieve from database.
    return render_template('index.html', editions=temp_editions), 200

@admin.route('/supremum/new', methods=["GET", "POST"])
def new_supremum():
    form = SupremumForm()
    if form.validate_on_submit():
        # Add supremum to database
        # TODO
        
        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("edit_supremum_form.html", form=form), 200

@admin.route('/supremum/edit/<int:sid>', methods=["GET", "POST"])
def edit_supremum(sid: int):
    # Retrieve the supremum with sid
    temp_supremum = {
            'theme': 'The Disaster Edition',
            'volume_nr': 52,
            'edition_nr': 0,
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'id': 0,
            'published': True
    }
    # TODO: retrieve from the database
    
    form = SupremumForm(supremum=temp_supremum)
    if form.validate_on_submit():
        # Update supremum in database...
        
        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("edit_supremum_form.html", form=form), 200
