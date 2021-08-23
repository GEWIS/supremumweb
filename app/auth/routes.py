from flask import render_template, request, abort, url_for, redirect
from flask_login import login_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

from app.auth import auth_bp as auth
from app.extensions import lm

from .forms import LoginForm
from app.auth.models import User


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)

        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return render_template(next or url_for('home.index'))
    return render_template('login.html', form=form), 200


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))
