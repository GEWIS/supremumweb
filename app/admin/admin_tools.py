from flask import current_app, request, Response
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.tools import code_page
from app.config import basedir
from functools import wraps
import os

def admin_required(func):
    @wraps(func)
    def validate_is_admin(*args, **kwargs):
        try:
            is_admin = current_user.is_admin
        except:
            is_admin = False
        finally:
            if not is_admin:
                return code_page(403, f"Sadly, only Supremum members are permitted on this page. Feel free to join us!")
        return func(*args, **kwargs)
    return validate_is_admin

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
        fname = f'supremum_{form.volume_nr.data}.{form.edition_nr.data}_cover.png'
        save_file(cover, fname)
        kwargs['filename_cover'] = fname

    return kwargs