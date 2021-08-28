from flask import render_template
from flask_login import current_user

def render(template, **kwargs):
    """Wraps the render_template function, but inserts default arguments"""
    kwargs.setdefault('user', current_user)
    return render_template(template, **kwargs)

def http_code(e):
    return code_page(e.code, e.name)

def code_page(code, message=""):
    return render('error_code.html', code=code, message=message), code
