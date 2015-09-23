# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.stations.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
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

    def test_api_stations_edit(self):
        url = url_for('api.stations', obj_id='test1')

        response = self.client.put(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'name': 'modified',
            'code': 'modified',
            'kind': ['test', 'modified'],
            'source': 'test1',
            'sensors': ['test1']
        }))

        self.assert200(response)

        station = Station.query.filter(Station.code == 'modified').first()
        self.assertIsNotNone(station)
        self.assertEquals(station.name, 'modified')
        self.assertEquals(station.kind, ['test', 'modified'])
        self.assertEquals(station.sensors[0].identifier, 'test1')
