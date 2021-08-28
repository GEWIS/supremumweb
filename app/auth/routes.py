from flask import request, url_for, redirect, Response, current_app
from flask_login import login_user, logout_user, current_user
from urllib.parse import urljoin

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
        return redirect(url_for('home.infimum_overview'))
    app_id = current_app.config['GEWIS_API_APPID']
    return redirect(urljoin('https://gewis.nl/token/', app_id))

@auth.route('/callback')
def callback():
    if current_user.is_authenticated:
        return redirect(url_for('home.infima_overview'))

    # Retrieve token from url
    jwt_str = request.args.get("token", None)
    if jwt_str is None:
        return Response("No token was provided", 401)

    # Validate token header
    try:
        header = jwt.get_unverified_header(jwt_str)
    except jwt.exceptions.DecodeError:
        return Response("Invalid token provided", 400)
    if "typ" not in header:
        return Response(f"Token type not specified.", 400)
    if header["typ"] != 'JWT':
        return Response(
            f"Invalid token type '{header['type']}'. Expected 'JWT'.", 400
        )
    if "alg" not in header:
        return Response(f"JWT algorithm not specified.", 400)
    alg = header['alg']

    # Decode token
    try:
        token = jwt.decode(
            jwt_str,
            key=current_app.config['GEWIS_API_KEY'],
            algorithms=[alg]
        )
    except jwt.exceptions.ExpiredSignatureError:
        return Response(f"Signature has expired. Please try again.", 401)
    except Exception as e:
        return Response(f"Something went wrong while logging you in: {str(e)}", 500)

    # Verify token's expiration date
    expiration = datetime.fromtimestamp(token['exp'])
    if expiration < datetime.now():
        return Response("JWT token has expired", 401)

    # Retrieve information from token
    lidnr = token['lidnr']
    user = User.get_by_id(lidnr)
    if user is None:
        user = User.create(id=lidnr, is_admin=False)

    login_user(user)

    # Redirect to infima overview page
    # TODO: can we do something a bit more custom?
    return redirect(url_for('home.infima_overview'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))
