# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.data.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from flask import url_for, json
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Station, Source, Sensor
from sih.modules.data.models import Data, SensorData


class ApiDataEditTestCase(TestCase):

    def setUp(self):
        super(ApiDataEditTestCase, self).setUp()

        source = Source(id=1, name='Test 1', identifier='test1')
        sensor = Sensor(id=1, identifier='test', name='Test',
                        measure_unit='mm')

        station = Station(name='Test 1',
                          code='test1',
                          kind=['pluviometric'],
                          source=source,
                          location=WKTElement('POINT(1 1)'),
                          altitude=10,
                          sensors=[sensor])

        data = Data(id=1, station=station,
                    read_at=datetime(1994, 10, 27, 8),
                    sensor_data=[SensorData(sensor=sensor, value=2)])

        db.session.add(data)

    def test_api_data_create(self):
        url = url_for('api.data', obj_id=1)

        response = self.client.put(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'read_at': '2015-09-23T22:04:51+03:00',
            'station': 'test1',
            'values': [{
                'sensor': 'test',
                'value': 10
            }]
        }))

        self.assert200(response)

        self.assertEquals(Data.query.count(), 1)

        data = Data.query.filter(Data.id == 1).first()
        self.assertEquals(data.values['test'], 10)
