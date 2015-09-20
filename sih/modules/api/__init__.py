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


api = Blueprint('api', __name__)


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


@api.route('/ping')
@role_required(['api'])
def ping():
    return jsonify({
        'pong': True
    })
