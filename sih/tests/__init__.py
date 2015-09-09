# -*- coding: utf-8 -*-
"""
    sih.tests
    ~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_testing import TestCase
from sih import create_app
from sih.config import TestingConfig
from sih.extensions import db


class TestCase(TestCase):

    def create_app(self):
        app = create_app(TestingConfig())
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.close()
