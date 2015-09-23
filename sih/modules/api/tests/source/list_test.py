# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.source.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Source


class ApiSourcesListTestCase(TestCase):

    def setUp(self):
        super(ApiSourcesListTestCase, self).setUp()

        source1 = Source(name='Test 1', identifier='test1')
        source2 = Source(name='Test 2', identifier='test2')
        source3 = Source(name='Test 3', identifier='test3')

        db.session.add(source1)
        db.session.add(source2)
        db.session.add(source3)

    def test_api_sources_list(self):
        url = url_for('api.sources')

        response = self.client.get(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)

        data = response.json
        self.assertEquals(len(data['data']), 3)
        self.assertEquals(data['summary']['total'], 3)
