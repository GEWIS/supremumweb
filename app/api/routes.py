from flask import jsonify, request, current_app, Response
from . import api_bp as api
from app.home.models import Infimum
from app.extensions import cache
import json


def make_json_response(data, code=200):
    return Response(json.dumps(data), mimetype='application/json', status=code)


@api.route('/random_infimum')
@cache.memoize(300)
def get_random_infimum():
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

    random_infimum = Infimum.get_random_infimum()
    if random_infimum is None:
        return make_json_response({
            "authenticated": True,
            "message": "No eligible infimum was found."
        }, 404)

    formatted_infimum = random_infimum.format_public()
    return jsonify(formatted_infimum), 200
