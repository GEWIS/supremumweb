from flask import url_for, redirect, abort, jsonify, request
from flask_login import login_required

from app.tools import code_page
from app.admin import admin_bp as admin
from app.admin.forms import SupremumForm, InfimumEditForm, InfimumAssignForm
from app.home.models import Supremum, Infimum

from app.tools import render
from .admin_tools import admin_required, retrieve_supremum_from_form


@admin.route('/')
@admin.route('/home')
@login_required
@admin_required
def index():
    sup_limit = int(request.args.get('nr_supremum', 5))
    editions = Supremum._get_editions(limit=sup_limit)
    inf_limit = int(request.args.get('nr_infima', 5))
    infima = Infimum._get_unassigned_infima(limit=inf_limit)
    return render('index.html',
                  editions=editions, all_editions=sup_limit == 0,
                  infima=infima, all_infima=inf_limit == 0), 200


@admin.route('/supremum/new', methods=["GET", "POST"])
@login_required
@admin_required
def new_supremum():
    form = SupremumForm()
    if form.validate_on_submit():
        kwargs = retrieve_supremum_from_form(form)

        # Add supremum to database
        Supremum.create(**kwargs)

        # Return to admin panel
        return redirect(url_for("admin.index"))
    return render("forms/new_supremum_form.html", form=form), 200


@admin.route('/supremum/<int:sid>/edit', methods=["GET", "POST"])
@login_required
@admin_required
def edit_supremum(sid: int):
    supremum = Supremum.get_by_id(sid)
    if supremum is None:
        return code_page(404, f"Supremum with id '{sid}' does not exist.")

    form = SupremumForm(supremum=supremum)
    if form.validate_on_submit():
        kwargs = retrieve_supremum_from_form(form)

        # Update supremum in database
        supremum.update(**kwargs)

        # Return to admin panel
        return redirect(url_for("admin.index"))

    form._populate()
    return render("forms/edit_supremum_form.html", form=form), 200


@admin.route('/supremum/<int:sid>/infima')
@login_required
@admin_required
def infima_of_supremum_edition_with_id(sid: int):
    supremum = Supremum.get_by_id(sid)
    if supremum is None:
        return code_page(404, f"Supremum with id '{sid}' does not exist.")

    infima = Infimum.get_infima_with_supremum_id(sid)
    return render("admin_infima_overview.html", supremum=supremum,
                  infima=infima), 200


@admin.route('/supremum/<int:sid>/infima/download')
@login_required
@admin_required
def download_infima_of_supremum_edition_with_id(sid: int):
    supremum = Supremum.get_by_id(sid)
    if supremum is None:
        return code_page(404, f"Supremum with id '{sid}' does not exist.")

    infima = Infimum.get_infima_with_supremum_id(sid)

    result = []
    for inf in infima:
        result.append(inf.content.replace("\r\n", "<br/>"))
        result.append('%')
    return "<br/>".join(result), 200


@admin.route('/infimum/<int:iid>/edit', methods=["GET", "POST"])
@login_required
@admin_required
def edit_infimum(iid: int):
    infimum = Infimum.get_infimum_with_id(iid)
    if infimum is None:
        return code_page(404, f"Infimum with id '{id}' does not exist.")

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
    return render("forms/edit_infimum_form.html", form=form), 200


@admin.route('/infima/assign', methods=["GET", "POST"])
@login_required
@admin_required
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
    return render("forms/assign_infima_form.html", form=form), 200
