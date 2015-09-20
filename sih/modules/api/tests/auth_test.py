# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.auth_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from base64 import b64encode
from flask import url_for
from sih.tests import TestCase


class ApiAuthTestCase(TestCase):

    def test_unauthenticated_request(self):
        response = self.client.get(url_for('api.ping'))

        self.assert401(response)
        self.assertEquals(response.json['message'], u'Bad credentials')

    def test_authenticated_request(self):
        auth = u'Basic {}'.format(b64encode('{}:{}'.format('admin', 'secret')))

        response = self.client.get(url_for('api.ping'), headers={
            'Authorization': auth
        })

        self.assert200(response)
