from flask import render_template, jsonify
from . import infima_bp
from .forms import SubmitForm


@infima_bp.route('/')
def infima_overview():
    return render_template('infima.html'), 200


@infima_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    form.infimum_text(placeholder="testtestestestse")
    if form.validate_on_submit():
        print("infimum:", form.infimum_text, form.infimum)
        return render_template('submit.html', success=True), 200
    return render_template('submit.html', form=form), 200
    # return render_template('submit.html', form=None), 200
