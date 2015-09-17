# -*- coding: utf-8 -*-
"""
    sih.modules.data.tests.views.stations.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source, Sensor
from sih.modules.data.models import Data, SensorData


class DeleteStationDataTestCase(TestCase):

    def test_permission_required(self):
        url = url_for('data.stations_delete', station_id=1, data_id=1)
        response = self.client.post(url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_delete_station_data(self):
        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')

        sensor = Sensor(identifier='test',
                        name='Test',
                        measure_unit='mm')

        station = Station(name='Test 1',
                          code='test1',
                          kind=['pluviometric'],
                          source=source,
                          location=WKTElement('POINT(-27 -45)'),
                          altitude=10,
                          sensors=[sensor])

        data = Data(read_at=datetime(1994, 1, 6),
                    received_at=datetime(1994, 1, 7),
                    station=station)

        sensor_data = SensorData(data=data, sensor=sensor, value=10)

        db.session.add(sensor_data)

        url = url_for('data.stations_delete', station_id=1, data_id=1)
        response = self.client.post(url)

        self.assertRedirects(response,
                             url_for('data.stations_view', station_id=1))
        self.assertEquals(Data.query.count(), 0)
