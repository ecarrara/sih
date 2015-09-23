# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.source.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Source


class ApiSourcesEditTestCase(TestCase):

    def test_api_source_edit(self):
        source = Source(name='Test', identifier='test')
        db.session.add(source)

        url = url_for('api.sources', obj_id='test')

        response = self.client.put(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'name': 'Test Modified',
            'identifier': 'modified',
            'url': 'http://example.com',
            'license': 'OpenData'
        }))

        self.assertEquals(response.status_code, 200)

        source = Source.query.filter(Source.identifier == 'modified').first()
        self.assertIsNotNone(source)
        self.assertEquals(source.name, 'Test Modified')
        self.assertEquals(source.url, 'http://example.com')
        self.assertEquals(source.license, 'OpenData')
