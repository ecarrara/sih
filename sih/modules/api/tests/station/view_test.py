# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.stations.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Station, Source, Sensor


class ApiStationsEditTestCase(TestCase):

    def setUp(self):
        super(ApiStationsEditTestCase, self).setUp()

        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')
        sensor = Sensor(name='Test', identifier='test1',
                        measure_unit='test')
        station = Station(name='Test 1', code='test1',
                          kind=['pluviometric'], source=source,
                          sensors=[])

        db.session.add(source)
        db.session.add(sensor)
        db.session.add(station)

    def test_api_stations_view(self):
        url = url_for('api.stations', obj_id='test1')

        response = self.client.get(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)

    def test_api_stations_view_not_found(self):
        url = url_for('api.stations', obj_id='test-not-found')

        response = self.client.get(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert404(response)

        self.assertEquals(response.json, {
            'message': 'Not found'
        })
