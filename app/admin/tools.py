from flask import current_app
from werkzeug.utils import secure_filename
import os

def save_file(f):
    fname = secure_filename(f.filename)
    path = os.path.join(os.getcwd(), current_app.config['DATA_PATH'], fname)
    with open(path, "wb") as file:
        file.write(f.stream.read())