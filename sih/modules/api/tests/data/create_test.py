# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.data.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Station, Source, Sensor
from sih.modules.data.models import Data


class ApiDataCreateTestCase(TestCase):

    def setUp(self):
        super(ApiDataCreateTestCase, self).setUp()

        source = Source(id=1, name='Test 1', identifier='test1')
        sensor = Sensor(id=1, identifier='test', name='Test',
                        measure_unit='mm',
                        validate_code='result = value > 0')

        station = Station(name='Test 1',
                          code='test1',
                          kind=['pluviometric'],
                          source=source,
                          location=WKTElement('POINT(1 1)'),
                          altitude=10,
                          sensors=[sensor])
        db.session.add(station)

    def test_api_data_create(self):
        url = url_for('api.data')

        response = self.client.post(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'read_at': '2015-09-23T22:04:51+03:00',
            'station': 'test1',
            'values': [{
                'sensor': 'test',
                'value': 2
            }]
        }))

        self.assertEquals(response.status_code, 201)

        self.assertEquals(Data.query.count(), 1)

    def test_api_data_invalid_sensor_value(self):
        url = url_for('api.data')

        response = self.client.post(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'read_at': '2015-09-23T22:04:51+03:00',
            'station': 'test1',
            'values': [{
                'sensor': 'test',
                'value': -2
            }]
        }))

        self.assertEquals(response.status_code, 400)
        self.assertEquals(Data.query.count(), 0)
