from flask import render_template, jsonify, abort, Response, request
from . import home_bp as home
from .forms import SubmitInfimumForm, InfimumSearchForm
from .models import Supremum, Infimum

from datetime import datetime


@home.route('/')
def index():
    latest_supremum = Supremum.get_latest_published_edition()
    return render_template('home.html', supremum=latest_supremum)


@home.route('/infimum', methods=['GET', 'POST'])
def infima_overview():
    inf_search_form = InfimumSearchForm()

    # Retrieve search results.
    infima = []
    if inf_search_form.validate_on_submit():
        seach_term = inf_search_form.search_term.data
        infima = Infimum.search_published_infima(seach_term)

    published_suprema = Supremum.get_published_editions()
    return render_template('infima_overview.html', suprema=published_suprema,
                           form=inf_search_form, search_results=infima)


@home.route('/infimum/submit', methods=['GET', 'POST'])
def submit():
    infimum_form = SubmitInfimumForm()

    # Save infimum when submitted
    if infimum_form.validate_on_submit():
        content = infimum_form.content.data
        submission_date = datetime.now()
        Infimum.create(content=content, submission_date=submission_date,
                       rejected=False)

        return render_template('submit.html', success=True), 200
    return render_template('submit.html', form=infimum_form), 200


@home.route('/supremum')
def supremum_overview():
    suprema = Supremum.get_published_editions()

    # Split suprema up per volume
    volumes = {}
    for supremum in suprema:
        volume = volumes.setdefault(supremum.volume_nr, [])
        volume.append(supremum)

    return render_template('archive.html', volumes=volumes)


@home.route('/supremum/<int:volume_nr>.<int:edition_nr>/infima')
def infima_for_edition(volume_nr, edition_nr):
    supremum = Supremum.get_supremum_by_volume_and_edition(
        volume_nr, edition_nr)
    if supremum is None or not supremum.published:
        abort(404)

    # Retrieve infima
    infima = Infimum.get_infima_with_supremum_id(supremum.id)

    return render_template('infima_edition.html', supremum=supremum,
                           infima=infima), 200
