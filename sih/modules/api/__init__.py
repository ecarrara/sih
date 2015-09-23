# -*- coding: utf-8 -*-
"""
    sih.modules.api
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user
from sih.permissions import role_required
from sih.modules.users.models import User
from sih.modules.api.views import ApiView
from sih.modules.api.resources.station import StationResource
from sih.modules.api.resources.sensor import SensorResource


api = Blueprint('api', __name__)


api_version = '0.0.1'


@api.after_request
def api_request(response):
    response.headers['X-API-Version'] = api_version
    return response


@api.before_request
def auth_user():
    auth = request.authorization
    if auth:
        user = User.query \
                   .filter(User.username == auth.username) \
                   .first()

        if user and user.api_key == request.authorization.password:
            login_user(user)
            return

    return jsonify({
        'message': 'Bad credentials'
    }), 401


@api.before_request
def check_content_type():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({
            'message': 'Wrong Content-Type, use application/json'
        })


@api.route('/ping')
@role_required(['api'])
def ping():
    return jsonify({
        'pong': True
    })


ApiView.register(api, 'stations', '/stations', StationResource())
ApiView.register(api, 'sensors', '/sensors', SensorResource())
