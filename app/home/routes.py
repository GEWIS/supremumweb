from flask import render_template, jsonify, url_for, abort, Response
from . import home_bp as home

from .forms import SubmitForm, SearchForm
from .models import Supremum, Infimum

import re
from datetime import datetime


@home.route('/')
def index():
    temp_edition = {
        'title': 'The Earth Edition',
        'img_url': url_for("home.static", filename="latest_edition.png"),
        'pdf_url': url_for("home.static", filename="latest_supremum.pdf"),
        'name': 'Supremum 53.0'
    }
    return render_template('home.html', edition=temp_edition)


@home.route('/infimum', methods=['GET', 'POST'])
def infima_overview():
    form = SearchForm()

    # Get search results if present.
    search_results = []
    if form.validate_on_submit():
        infima = Infimum.safe_search(form.search_term.data)
        search_results = [inf.format_public() for inf in infima]

    # Get editions
    suprema = Supremum.get_all_published_editions()
    editions = [sup.format_public() for sup in suprema]

    return render_template('infima_overview.html', editions=editions,
                           form=form, search_results=search_results), 200


@home.route('/infimum/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        content = form.infimum_text.data
        submission_date = datetime.now()
        Infimum.create(content=content,
                       submission_date=submission_date, rejected=False)
        return render_template('submit.html', success=True), 200
    return render_template('submit.html', form=form), 200


@home.route('/infimum/random')
def get_random_infimum():
    random_infimum = Infimum.get_random_infimum()
    if random_infimum is None:
        return jsonify({"msg": "No eligible infimum was found"}), 404

    formatted_infimum = random_infimum.format_public()
    return jsonify(formatted_infimum), 200


@home.route('/supremum')
def supremum_overview():
    suprema = Supremum.get_all_published_editions()
    volumes = {}
    for supremum in suprema:
        volumes.setdefault(supremum.volume_nr, []).append(
            supremum.format_public())
    return render_template('archive.html', volumes=volumes)


@home.route('/supremum/<int:volume_nr>.<int:edition_nr>/infima')
def infima_for_edition(volume_nr, edition_nr):
    # Retrieve supremum based on edition information.
    try:
        supremum = Supremum.get_supremum_by_volume_and_edition(
            volume_nr, edition_nr)
        if supremum is None:
            raise ValueError("This edition does not exist")
    except Exception as e:
        return abort(Response(str(e)))

    # Retrieve infima
    results = Infimum.get_infima_with_supremum_id(supremum.id)
    infima = [inf.format_public() for inf in results]

    return render_template('infima_edition.html', infima=infima,
                           volume_nr=volume_nr, edition_nr=edition_nr), 200
