# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.data.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from datetime import datetime
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Station, Source, Sensor
from sih.modules.data.models import Data, SensorData


class ApiDataListTestCase(TestCase):

    def setUp(self):
        super(ApiDataListTestCase, self).setUp()

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

    def test_api_data_list(self):
        url = url_for('api.data')

        response = self.client.get(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)

        data = response.json
        self.assertEquals(len(data['data']), 1)
        self.assertEquals(data['summary']['total'], 1)

    def test_api_data_filters(self):
        url = url_for('api.data')

        response = self.client.get(url, query_string={
            'start': datetime(1994, 10, 27, 6).isoformat(),
            'end': datetime(1994, 10, 27, 12).isoformat(),
            'station': 'test1',
            'kind': 'pluviometric',
            'sensor': 'test',
            'bbox': '0,0,2,2',
            'source': 'test1'
        }, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)

        data = response.json
        self.assertEquals(len(data['data']), 1)
        self.assertEquals(data['summary']['total'], 1)
