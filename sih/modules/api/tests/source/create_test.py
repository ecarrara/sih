# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.source.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Source


class ApiSourcesCreateTestCase(TestCase):

    def test_api_source_create(self):
        url = url_for('api.sources')

        response = self.client.post(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'name': 'Example',
            'identifier': 'example',
            'url': 'http://example.com',
            'license': 'OpenData'
        }))

        self.assertEquals(response.status_code, 201)

        source = Source.query.filter(Source.identifier == 'example').first()
        self.assertIsNotNone(source)
        self.assertEquals(source.name, 'Example')
        self.assertEquals(source.identifier, 'example')
        self.assertEquals(source.url, 'http://example.com')
        self.assertEquals(source.license, 'OpenData')

    def test_api_source_create_without_name(self):
        url = url_for('api.sources')

        response = self.client.post(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'identifier': 'example',
            'url': 'http://example.com',
            'license': 'OpenData'
        }))

        self.assertEquals(response.status_code, 400)
