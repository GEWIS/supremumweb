from flask import abort, redirect, current_app
from flask_login import login_required, current_user
from . import home_bp as home

from .forms import SubmitInfimumForm, InfimumSearchForm
from .models import Supremum, Infimum
from app.tools import code_page
from app.tools import render

from datetime import datetime, date, timedelta


@home.route('/')
def index():
    latest_supremum = Supremum.get_latest_published_edition()
    return render('home.html', supremum=latest_supremum)


@home.route('/infimum', methods=['GET', 'POST'])
@login_required
def infima_overview():
    inf_search_form = InfimumSearchForm()

    # Retrieve search results.
    infima = []
    if inf_search_form.validate_on_submit():
        search_term = inf_search_form.search_term.data
        infima = Infimum.search_published_infima(search_term)

    published_suprema = Supremum.get_published_editions()
    return render('infima_overview.html', suprema=published_suprema,
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

        return render('submit.html', success=True), 200
    return render('submit.html', form=infimum_form), 200


@home.route('/supremum')
def supremum_overview():
    suprema = Supremum.get_published_editions()

    # Split suprema up per volume
    volumes = {}
    for supremum in suprema:
        volume = volumes.setdefault(supremum.volume_nr, [])
        volume.append(supremum)

    # Sort volumes
    for volume_nr, editions in volumes.items():
        volumes[volume_nr] = sorted(editions, key=lambda x: x.edition_nr,
                                    reverse=True)

    return render('archive.html', volumes=volumes)


@home.route('/supremum/<int:volume_nr>.<int:edition_nr>')
def supremum_by_volume_nr_and_edition_nr(volume_nr, edition_nr):
    supremum = Supremum.get_by_volume_and_edition(volume_nr, edition_nr)
    if supremum is None or not supremum.published:
        return code_page(404, f'Supremum {volume_nr}.{edition_nr} does not (yet) exist.')
    return redirect(supremum.pdf_url)


@home.route('/supremum/<int:volume_nr>.<int:edition_nr>/infima')
@login_required
def infima_for_edition(volume_nr, edition_nr):
    supremum = Supremum.get_by_volume_and_edition(volume_nr, edition_nr)
    if supremum is None or not supremum.published:
        return code_page(404, f'Supremum {volume_nr}.{edition_nr} does not (yet) exist.')

    # Retrieve infima
    infima = Infimum.get_infima_with_supremum_id(supremum.id)

    return render('infima_edition.html', supremum=supremum,
                  infima=infima, user=current_user), 200


@home.route('/writing/manual')
def writers_manual():
    wm_url = current_app.config['WRITER_MANUAL_URL']
    print("url", wm_url)
    if not wm_url:
        return abort(404)
    return redirect(wm_url)


@home.route('/calendar')
def puzzle_answers():
    # Find all Sundays of 2023
    d = date(2023, 1, 1)                    # January 1st
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    sundays = []
    while d.year == 2023:
        sundays.append(d)
        d += timedelta(days = 7)

    # Find the most recent sunday
    today = date.today()
    idx = today.weekday()
    if idx == 6:
        most_recent_sunday = today
    else:
        most_recent_sunday = today - timedelta(7+idx-6)

    # Get all the ordinal numbers
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    ordinals = [ordinal(n) for n in range(1,32)]

    # Get all the months
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Get a list of published puzzle answers
    # TODO: Update this list automatically based on the contents of the 'puzzles' folder
    published = ["1-1"]

    return render('puzzle_answers.html', all_sundays=sundays, most_recent_puzzle_date=most_recent_sunday, ordinals=ordinals, months=months, published_puzzles=published)


@home.route('/calendar/puzzle/<int:month_nr>/<int:day_nr>')
def puzzle(month_nr, day_nr):
    puzzle = 'puzzles/puzzle{}-{}.html'.format(str(month_nr).zfill(2), str(day_nr).zfill(2))
    return render(puzzle)
