# -*- coding: utf-8 -*-
"""
    sih.tests
    ~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from functools import wraps
from flask import url_for
from flask_testing import TestCase
from sih import create_app
from sih.config import TestingConfig
from sih.extensions import db, assets, login_manager
from sih.modules.users.models import User


class TestCase(TestCase):

    def create_app(self):
        assets._named_bundles = {}
        app = create_app(TestingConfig())
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

        admin = User(name='Admin', username='admin',
                     email='admin@example.com', password='test',
                     status='active', roles=['admin', 'api'],
                     api_key='secret')

        db.session.add(admin)

    def tearDown(self):
        db.session.close()


def logged_as(username, password):
    def decorator(fn):
        @wraps(fn)
        def decorated_fn(self, *args, **kwargs):
            self.client.post(url_for(login_manager.login_view), data={
                'username': username,
                'password': password
            })
            fn(self, *args, **kwargs)

        return decorated_fn

    return decorator
