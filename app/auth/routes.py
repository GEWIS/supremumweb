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
    return redirect(urljoin('https://gewis.nl/user/token/', app_id))

@auth.route('/callback')
def callback():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    # Retrieve token from url
    jwt_str = request.args.get("token", None)
    if jwt_str is None:
        return code_page(401, "No login token was provided with this callback.")

    # Decode token. GEWIS signs tokens for shared-secret apps with HS512; the algorithm is pinned rather than read
    # from the (unverified) header. The header carries no `typ`, which is optional per RFC 7515.
    try:
        token = jwt.decode(
            jwt_str,
            key=current_app.config['GEWIS_API_KEY'],
            algorithms=['HS512'],
            options={'require': ['exp', 'sub']},
        )
    except jwt.exceptions.ExpiredSignatureError:
        return code_page(401, f'The signature on your login token has expired. Please log in again.')
    except jwt.exceptions.InvalidTokenError as e:
        return code_page(401, f'Your login token is invalid: {str(e)}')

    # Verify token's expiration date
    expiration = datetime.fromtimestamp(token['exp'])
    if expiration < datetime.now():
        return code_page(400, f'Your login token as expired. Please log in again.')

    # Retrieve information from token
    # `sub` identifies the member; the `lidnr` claim is deprecated by GEWIS.
    lidnr = int(token['sub'])
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
