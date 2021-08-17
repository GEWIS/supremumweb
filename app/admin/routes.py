from flask import render_template, url_for, redirect
from flask_login import login_required
from datetime import datetime

from app.admin import admin_bp as admin
from app.admin.forms import SupremumForm, InfimumEditForm, InfimumAssignForm

@admin.route('/')
@admin.route('/home')
# @login_required
def index():
    temp_editions = [
        {
            'title': 'The Fire Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.1',
            'id': 5,
            'published': True
        },
        {
            'title': 'The Wind Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.1',
            'id': 4,
            'published': True
        },
        {
            'title': 'The Earth Edition',
            # 'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.0',
            'id': 3
        },
        {
            'title': 'The Default Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            # 'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
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
    
    temp_infima = [
        {
            'id': 1,
            'content': "Hahah wat een grap! Ik ga even testen hoe lang ik deze zin kan maken.\n Wat denken we eravn?",
            'submission_date': "2021-08-11",
            'rejected': False
        },
        {
            'id': 2,
            'content': "Blarb blarb!",
            'submission_date': "2021-08-11",
            'rejected': True
        }
        ]
    
    return render_template('index.html', editions=temp_editions, infima=temp_infima), 200

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

@admin.route('/infimum/<int:iid>/edit', methods=["GET", "POST"])
def edit_infimum(iid: int):
     # Retrieve the infimum with iid
    temp_infimum = {
        'id': iid,
        'content': 'Haha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\n',
        'rejected': False,
        'creation_date': datetime.fromisoformat('2021-08-11')
    }
    # TODO: retrieve from the database
    
    form = InfimumEditForm(infimum=temp_infimum)
    if form.validate_on_submit():
        # Update infimum in database...
        
        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("edit_infimum_form.html", form=form), 200

@admin.route('/infimum/assign', methods=["GET", "POST"])
def assign_infima():
    temp_infima = [
        {
            'id': 0,
            'content': 'Haha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\n',
            'rejected': False,
            'creation_date': datetime.fromisoformat('2021-08-11')
        },
        {
            'id': 1,
            'content': 'Haha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\nHaha, this is a test :D\n What do we think?\nOk, this is just to check the overflow...\n',
            'rejected': False,
            'creation_date': datetime.fromisoformat('2021-08-11')
        }
    ]
    
    temp_suprema = [
        {
            'theme': 'The Fire Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.1',
            'id': 5,
            'published': True
        },
        {
            'theme': 'The Wind Edition',
            'img_url' : url_for("home.static", filename="latest_edition.png"),
            'pdf_url' : url_for("home.static", filename="latest_supremum.pdf"),
            'name': 'Supremum 53.1',
            'id': 4,
            'published': True
        }
    ]
    # TODO: retrieve from the database
    
    form = InfimumAssignForm(infima=temp_infima, suprema=temp_suprema)
    if form.validate_on_submit():
        # Update infimum in database...
        
        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("assign_infima_form.html", form=form), 200

@admin.route('/infima/<int:sid>')
def infima_of_supremum_edition_with_id(sid: int):
    temp_infima = [
        {
            'id': 1,
            'content': "Hahah wat een grap! Ik ga even testen hoe lang ik deze zin kan maken.\n Wat denken we eravn?",
            'submission_date': "2021-08-11",
            'rejected': False
        },
        {
            'id': 2,
            'content': "Blarb blarb!",
            'submission_date': "2021-08-11",
            'rejected': True
        }
    ]

    return render_template("infima_overview.html", infima=temp_infima), 200
    