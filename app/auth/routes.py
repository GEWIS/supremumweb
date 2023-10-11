from flask import request, url_for, redirect, Response, current_app
from flask_login import login_user, logout_user, current_user
from urllib.parse import urljoin

from app.tools import code_page
from app.auth import auth_bp as auth
from app.auth.models import User
from app.extensions import lm

import jwt
from datetime import datetime


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    app_id = current_app.config['GEWIS_API_APPID']
    return redirect(urljoin('https://gewis.nl/token/', app_id))

@auth.route('/callback')
def callback():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    # Retrieve token from url
    jwt_str = request.args.get("token", None)
    if jwt_str is None:
        return code_page(401, "No login token was provided with this callback.")

    # Validate token header
    try:
        header = jwt.get_unverified_header(jwt_str)
    except jwt.exceptions.DecodeError:
        return code_page(400, 'The provided login token has an invalid format')
    if "typ" not in header:
        return code_page(400, 'Your login token did does not specify its type')
    if header["typ"] != 'JWT':
        return code_page(400, f'Your login token type, {header["typ"]}, is not supported.')
    if "alg" not in header:
        return code_page(400, f'Your login token does not specify its HMAC algorithm.')
    alg = header['alg']

    # Decode token
    try:
        token = jwt.decode(
            jwt_str,
            key=current_app.config['GEWIS_API_KEY'],
            algorithms=[alg]
        )
    except jwt.exceptions.ExpiredSignatureError:
        return code_page(401, f'The signature on your login token has expired. Please log in again.')
    except Exception as e:
        return code_page(500, f'Something went wrong while logging you in: {str(e)}')

    # Verify token's expiration date
    expiration = datetime.fromtimestamp(token['exp'])
    if expiration < datetime.now():
        return code_page(400, f'Your login token as expired. Please log in again.')

    # Retrieve information from token
    lidnr = token['lidnr']
    user = User.get_by_id(lidnr)
    if user is None:
        user = User.create(id=lidnr, is_admin=False)

    login_user(user)

    if user.is_admin:
        return redirect(url_for('admin.index'))

    # Redirect to infima overview page
    # TODO: can we do something a bit more custom?
    return redirect(url_for('home.index'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))
