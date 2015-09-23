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

        source = Source(name='Test 1', identifier='test1')

        db.session.add(source)

    def test_api_sources_list(self):
        url = url_for('api.sources', obj_id='test1')

        response = self.client.get(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)
