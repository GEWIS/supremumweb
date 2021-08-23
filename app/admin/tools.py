from flask import current_app, request
from werkzeug.utils import secure_filename
from app.config import basedir
import os

def save_file(f, fname=None):
    if fname is None:
        fname = secure_filename(f.filename)
    path = os.path.join(basedir, current_app.config['DATA_PATH'], fname)
    with open(path, "wb") as file:
        file.write(f.stream.read())
    return fname

def retrieve_supremum_from_form(form):
    # Retrieve values from form
    kwargs = {
        'volume_nr': form.volume_nr.data,
        'edition_nr': form.edition_nr.data,
        'theme': form.theme.data,
        'published': form.published.data
    }

    # Update pdf
    pdf = request.files.getlist(form.magazine.name)[0]
    if pdf:
        fname = f'supremum_{form.volume_nr.data}.{form.edition_nr.data}_magazine.pdf'
        save_file(pdf, fname)
        kwargs['filename_pdf'] = fname

    # Update cover
    cover = request.files.getlist(form.cover.name)[0]
    if cover:
        fname = f'supremum_{form.volume_nr.data}.{form.edition_nr.data}_cover.pdf'
        save_file(cover, fname)
        kwargs['filename_cover'] = fname

    return kwargs