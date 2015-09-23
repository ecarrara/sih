# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.source.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Source


class ApiSourcesDeleteTestCase(TestCase):

    def setUp(self):
        super(ApiSourcesDeleteTestCase, self).setUp()

        source = Source(name='Test', identifier='test1')
        db.session.add(source)

    def test_api_stations_delete(self):
        url = url_for('api.sources', obj_id='test1')

        response = self.client.delete(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Source.query.count(), 0)

    def test_api_stations_delete_not_found(self):
        url = url_for('api.sources', obj_id='test-not-found')

        response = self.client.delete(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assertEquals(response.status_code, 404)
