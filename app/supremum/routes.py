from flask import render_template, jsonify, url_for
from . import supremum_bp as supremum

from .models import Supremum


@supremum.route('')
def supremum_overview():
    suprema = Supremum.get_all_published_editions()
    volumes = {}
    for supremum in suprema:
        volumes.setdefault(supremum.volume_nr, []).append(supremum.format_public())
    return render_template('archive.html', volumes=volumes)
