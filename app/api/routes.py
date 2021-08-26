from flask import jsonify, request, current_app, Response
from . import api_bp as api

from app.home.models import Infimum, Supremum
from app.extensions import cache

import json
from datetime import datetime
from functools import wraps


def make_json_response(data, code=200):
    return jsonify(data), code


def validate_key(func):
    @wraps(func)
    def validate(*args, **kwargs):
        key = request.args.get("key", None)
        if key is None:
            return make_json_response({
                'authenticated': False,
                'message': 'No key provided.'
            }, 401)
        if key != current_app.config['INFIMUM_API_KEY']:
            return make_json_response({
                'authenticated': False,
                'message': 'Provided key is invalid.'
            }, 401)
        return func(*args, **kwargs)
    return validate


@api.route('/random_infimum')
@validate_key
@cache.memoize(300)  # cache for 300 seconds
def get_random_infimum():
    random_infimum = Infimum.get_random_infimum()
    if random_infimum is None:
        return make_json_response({
            "authenticated": True,
            "message": "No eligible infimum was found."
        }, 404)

    formatted_infimum = random_infimum.format_public()
    return jsonify(formatted_infimum), 200


@api.route('/infimum/submit', methods=['POST'])
@validate_key
def submit_infimum():
    data = request.data
    if data is None:
        return make_json_response({
            "authenticated": True,
            "message": "No data was received."
        }, 400)

    try:
        infimum_data = json.loads(data)
    except:
        return make_json_response({
            "authenticated": True,
            "message": "Infimum was not given in json format."
        }, 400)

    if not 'content' in infimum_data:
        return make_json_response({
            "authenticated": True,
            "message": "Content was not provided."
        }, 400)

    content = infimum_data['content'].strip()
    infimum = Infimum.get_infimum_with_content(content)
    if infimum is not None:
        return make_json_response({
            "authenticated": True,
            "message": "This infimum already exists."
        }, 409)

    supremum_id = infimum_data.get('supremum_id', None)
    if supremum_id is not None:
        supremum = Supremum.get_by_id(supremum_id)
        if supremum is None:
            return make_json_response({
            "authenticated": True,
            "message": "No supremum with supremum_id exists."
        }, 404)

    if 'submission_date' in infimum_data:
        submission_date = datetime.strptime(
            infimum_data.get('submission_date'),
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        submission_date = datetime.now()

    kwargs = {
        'supremum_id': supremum_id,
        'content': content,
        'submission_date': submission_date,
        'rejected': infimum_data.get('rejected', False)
    }
    infimum = Infimum.create(**kwargs)
    return jsonify({"message": "Success", "infimum": infimum.format_public()}), 200
