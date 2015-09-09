# -*- coding: utf-8 -*-
"""
    sih.tests
    ~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_testing import TestCase
from sih import create_app
from sih.config import TestingConfig


class TestCase(TestCase):

    def create_app(self):
        app = create_app(TestingConfig())
        return app
