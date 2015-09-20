# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.auth_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase
from sih.modules.api.auth import basic_auth


class ApiAuthTestCase(TestCase):

    def test_unauthenticated_request(self):
        response = self.client.get(url_for('api.ping'), headers={
            'Content-Type': 'application/json'
        })

        self.assert401(response)
        self.assertEquals(response.json['message'], u'Bad credentials')

    def test_authenticated_request(self):
        response = self.client.get(url_for('api.ping'), headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)
