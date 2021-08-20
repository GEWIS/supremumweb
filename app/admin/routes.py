from flask import render_template, url_for, redirect, abort, request
from flask_login import login_required
from datetime import datetime

from app.admin import admin_bp as admin
from app.admin.forms import SupremumForm, InfimumEditForm, InfimumAssignForm
from app.home.models import Supremum, Infimum


@admin.route('/')
@admin.route('/home')
# @login_required
def index():
    editions = Supremum._get_all_editions()
    editions = [ed.format_private() for ed in editions]

    infima = Infimum._get_all_unassigned_infima()
    infima = [inf.format_private() for inf in infima]

    return render_template('index.html', editions=editions, infima=infima), 200

@admin.route('/supremum/new', methods=["GET", "POST"])
def new_supremum():
    form = SupremumForm()
    if form.validate_on_submit():
        # Retrieve values from form
        volume_nr = form.volume_nr.data
        edition_nr = form.edition_nr.data
        theme = form.theme.data
        published = form.published.data
        # TODO: retrieve .pdf and .png

        # Add supremum to database
        Supremum.create(volume_nr=volume_nr, edition_nr=edition_nr, theme=theme, published=published)

        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("forms/edit_supremum_form.html", form=form), 200

@admin.route('/supremum/<int:sid>/edit', methods=["GET", "POST"])
def edit_supremum(sid: int):
    supremum = Supremum.get_supremum_by_id(sid)
    if supremum is None:
        return abort(404)

    do_prepopulate = request.method == "GET"
    form = SupremumForm(supremum=supremum.format_private(), prepopulate=do_prepopulate)
    if form.validate_on_submit():
        # Retrieve data from form
        volume_nr = form.volume_nr.data
        edition_nr = form.edition_nr.data
        theme = form.theme.data
        published = form.published.data
        # TODO: retrieve pdf and cover png and handle appropriately

        # Update supremum in database
        supremum.update(volume_nr=volume_nr, edition_nr=edition_nr, theme=theme, published=published)

        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("forms/edit_supremum_form.html", form=form), 200

@admin.route('/supremum/<int:sid>/infima')
def infima_of_supremum_edition_with_id(sid: int):
    infima = Infimum.get_infima_with_supremum_id(sid)
    infima = [inf.format_private() for inf in infima]
    return render_template("admin_infima_overview.html", infima=infima), 200

@admin.route('/infimum/<int:iid>/edit', methods=["GET", "POST"])
def edit_infimum(iid: int):
    infimum = Infimum.get_infimum_with_id(iid)
    if infimum is None:
        return abort(404)

    suprema = Supremum._get_all_editions()
    editions = [(sup.id, str(sup)) for sup in suprema]

    do_prepopulate = request.method == "GET"
    form = InfimumEditForm(infimum=infimum.format_private(), suprema=editions, prepopulate=do_prepopulate)
    if form.validate_on_submit():
        # Retrieve data from form
        content = form.content.data
        supremum_id = form.supremum.data
        rejected = form.rejected.data

        # Update infimum in database...
        infimum.update(content=content, rejected=rejected, supremum_id=supremum_id)

        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("forms/edit_infimum_form.html", form=form), 200

@admin.route('/infima/assign', methods=["GET", "POST"])
def assign_infima():
    infima = Infimum._get_all_unassigned_infima()
    infs = [inf.format_private() for inf in infima]
    suprema = Supremum._get_all_editions()

    form = InfimumAssignForm(infima=infs, suprema=suprema)
    if form.validate_on_submit():
        # Update infimum in database...
        infima_ids = form.infima.data
        supremum_id = form.supremum.data

        # Update database
        for inf in infima:
            if inf.id in infima_ids:
                inf.update(supremum_id=supremum_id)

        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("forms/assign_infima_form.html", form=form), 200