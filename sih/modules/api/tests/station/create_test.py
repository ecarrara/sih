# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.stations.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Station, Source, Sensor


class ApiStationsCreateTestCase(TestCase):

    def setUp(self):
        super(ApiStationsCreateTestCase, self).setUp()

        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')
        sensor = Sensor(name='Test 1', identifier='test1',
                        measure_unit='test')

        db.session.add(source)
        db.session.add(sensor)

    def test_api_stations_create(self):
        url = url_for('api.stations')

        response = self.client.post(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'name': 'test',
            'code': 'test',
            'kind': ['test'],
            'source': 'test1',
            'sensors': ['test1']
        }))

        self.assertEquals(response.status_code, 201)

        station = Station.query.filter(Station.code == 'test').first()
        self.assertIsNotNone(station)
        self.assertEquals(station.name, 'test')
        self.assertEquals(station.kind, ['test'])
        self.assertEquals(station.sensors[0].identifier, 'test1')
        self.assertEquals(station.source.identifier, 'test1')

    def test_api_stations_create_invalid_schema(self):
        url = url_for('api.stations')

        response = self.client.post(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'name': 'test'
        }))

        self.assertEquals(response.status_code, 400)
