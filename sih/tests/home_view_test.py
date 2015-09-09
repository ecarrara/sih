# -*- coding: utf-8 -*-
"""
    sih.tests.home_view_test
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.tests import TestCase


class HomeViewTestCase(TestCase):

    def test_home_should_returns_valid_response(self):
        response = self.client.get('/')
        self.assert200(response)
