from flask import render_template
from flask_login import current_user

def render(template, **kwargs):
    """Wraps the render_template function, but inserts default arguments"""
    kwargs.setdefault('user', current_user)
    return render_template(template, **kwargs)