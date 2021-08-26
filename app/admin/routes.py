from flask import render_template, url_for, redirect, abort, request, jsonify
from flask_login import login_required

from app.admin import admin_bp as admin
from app.admin.forms import SupremumForm, InfimumEditForm, InfimumAssignForm
from app.home.models import Supremum, Infimum
from . import tools


@admin.route('/')
@admin.route('/home')
# @login_required
def index():
    editions = Supremum._get_editions_in_order()
    infima = Infimum._get_unassigned_infima()
    return render_template('index.html', editions=editions, infima=infima), 200


@admin.route('/supremum/new', methods=["GET", "POST"])
# @login_required
def new_supremum():
    form = SupremumForm()
    if form.validate_on_submit():
        kwargs = tools.retrieve_supremum_from_form(form)

        # Add supremum to database
        Supremum.create(**kwargs)

        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("forms/edit_supremum_form.html", form=form), 200


@admin.route('/supremum/<int:sid>/edit', methods=["GET", "POST"])
# @login_required
def edit_supremum(sid: int):
    supremum = Supremum.get_by_id(sid)
    if supremum is None:
        return abort(404)

    form = SupremumForm(supremum=supremum)
    if form.validate_on_submit():
        kwargs = tools.retrieve_supremum_from_form(form)

        # Update supremum in database
        supremum.update(**kwargs)

        # Return to admin panel
        return redirect(url_for("admin.index"))

    form._populate()
    return render_template("forms/edit_supremum_form.html", form=form), 200


@admin.route('/supremum/<int:sid>/infima')
# @login_required
def infima_of_supremum_edition_with_id(sid: int):
    supremum = Supremum.get_by_id(sid)
    if supremum is None:
        return abort(404)

    infima = Infimum.get_infima_with_supremum_id(sid)
    return render_template("admin_infima_overview.html", supremum=supremum,
                           infima=infima), 200


@admin.route('/supremum/<int:sid>/infima/download')
# @login_required
def download_infima_of_supremum_edition_with_id(sid: int):
    supremum = Supremum.get_by_id(sid)
    if supremum is None:
        return abort(404)

    infima = Infimum.get_infima_with_supremum_id(sid)
    return jsonify([inf.format_public() for inf in infima]), 200


@admin.route('/infimum/<int:iid>/edit', methods=["GET", "POST"])
# @login_required
def edit_infimum(iid: int):
    infimum = Infimum.get_infimum_with_id(iid)
    if infimum is None:
        return abort(404)

    suprema = Supremum._get_editions()
    form = InfimumEditForm(infimum=infimum, suprema=suprema)
    if form.validate_on_submit():
        # Retrieve data from form
        content = form.content.data
        supremum_id = form.supremum.data
        rejected = form.rejected.data

        # Update infimum in database...
        infimum.update(content=content, rejected=rejected,
                       supremum_id=supremum_id)

        # Return to admin panel
        return redirect(url_for("admin.index"))

    # Populate infimum fields
    form._populate()
    return render_template("forms/edit_infimum_form.html", form=form), 200


@admin.route('/infima/assign', methods=["GET", "POST"])
# @login_required
def assign_infima():
    infima = Infimum._get_unassigned_infima()
    suprema = Supremum._get_editions()

    form = InfimumAssignForm(infima=infima, suprema=suprema)
    if form.validate_on_submit():
        # Retrieve data from form
        infima_ids = form.infima.data
        supremum_id = form.supremum.data

        # Update infima
        for inf in infima:
            if inf.id in infima_ids:
                inf.update(supremum_id=supremum_id)

        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render_template("forms/assign_infima_form.html", form=form), 200
