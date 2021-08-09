from flask import render_template, jsonify, abort
from . import infima_bp as infima

from app.infima.forms import SubmitForm, SearchForm
from app.infima.models import Infimum

import re

@infima.route('/', methods=['GET', 'POST'])
def infima_overview():
    form = SearchForm()
    if form.validate_on_submit():
        print(form.search_term.data)
        # TODO: search for the term
        search_results = [{
            "self": "/infima/53.0#50",
            "id": 50,
            "content": 'This... this is a test haha and now Im just writing a long string for testing purposes.',
            "volume_nr": 53,
            "edition_nr": 0,
            "theme": "The Earth Edition"
        }]
    else:
        search_results = []
        
    # TODO: get editions.
    temp_editions = [
        {
            "volume_nr": 53,
            "edition_nr": 0,
            "theme": "The Earth Edition"
        },
        {
            "volume_nr": 53,
            "edition_nr": 1,
            "theme": "The Wind Edition"
        }
    ]
    
    return render_template(
        'infima_overview.html', 
        editions=temp_editions,
        form=form,
        search_results=search_results), 200


@infima.route('/<string:edition>')
def infima_for_edition(edition):
    try:
        res = re.match('(?P<volume_nr>\d*).(?P<edition_nr>\d)\Z', edition)
        volume_nr, edition_nr = res.group('volume_nr'), res.group('edition_nr')
    except Exception as e:
        return abort(404)
    
    # TODO: add check that edition is available !
    
    # try:
    #     infima = Infimum.query.filter_by(
    #         volume_nr=volume_nr, 
    #         edition_nr=edition_nr,
    #         rejected=0
    #     )
    # except Exception as e:
    #     return abort(500)
    
    test_infima = [
        {
            "id": 1,
            "supremum_id": 1,
            "content": "Erik en Leon zijn de supremum website aan het maken",
            "submission_date": "2021-05-27",
            "rejected": 0
        },
        {
            "id": 2,
            "supremum_id": 2,
            "content": "Erik en Leon zijn nog meer supremum website aan het maken",
            "submission_date": "2021-05-27",
            "rejected": 0
        }
    ]
    
    return render_template(
        'infima_edition.html', 
        infima=test_infima,
        volume_nr=volume_nr,
        edition_nr=edition_nr
    ), 200

@infima.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        print("infimum:", form.infimum_text, form.infimum)
        return render_template('submit.html', success=True), 200
    return render_template('submit.html', form=form), 200    

@infima.route('/random_infimum')
def get_random_infimum():
    first_infimum = dict(Infimum.query.first())
    return jsonify(first_infimum), 200