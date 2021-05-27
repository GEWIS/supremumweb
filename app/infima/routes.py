from flask import render_template, jsonify
from . import infima_bp as infima

from app.infima.forms import SubmitForm
from app.infima.models import Infimum

@infima.route('/')
def infima_overview():
    return render_template('infima.html'), 200


@infima.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    form.infimum_text(placeholder="testtestestestse")
    if form.validate_on_submit():
        print("infimum:", form.infimum_text, form.infimum)
        return render_template('submit.html', success=True), 200
    return render_template('submit.html', form=form), 200
    # return render_template('submit.html', form=None), 200

@infima.route('/random_infimum')
def get_random_infimum():
    first_infimum = dict(Infimum.query.first())
    return jsonify(first_infimum), 200