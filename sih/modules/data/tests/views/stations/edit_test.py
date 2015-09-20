# -*- coding: utf-8 -*-
"""
    sih.modules.data.tests.views.stations.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source, Sensor
from sih.modules.data.models import Data, SensorData


class EditStationDataTestCase(TestCase):

    def setUp(self):
        super(EditStationDataTestCase, self).setUp()

        source = Source(id=1, name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')

        sensor = Sensor(id=1,
                        identifier='test',
                        name='Test',
                        measure_unit='mm',
                        process_code='result = value * 2',
                        validate_code='result = value >= 0')

        station = Station(name='Test 1',
                          code='test1',
                          kind=['pluviometric'],
                          source=source,
                          location=WKTElement('POINT(-27 -45)'),
                          altitude=10,
                          sensors=[sensor])

        data = Data(id=1, station=station, read_at=datetime(1994, 10, 27, 8),
                    sensor_data=[SensorData(sensor=sensor, value=2)])

        db.session.add(station)
        db.session.add(data)

    def test_permission_required(self):
        url = url_for('data.stations_create', station_id=1)
        response = self.client.post(url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_edit_station_data(self):
        url = url_for('data.stations_edit', station_id=1, data_id=1)

        response = self.client.post(url, data={
            'station': 1,
            'read_at': '2012-10-27T08:00',
            'sensor_data-0-sensor': 1,
            'sensor_data-0-value': 5
        })

        self.assertRedirects(response,
                             url_for('data.stations_view', station_id=1))

        self.assertEquals(Data.query.count(), 1)

        data = Data.query.filter(Data.station_id == 1).first()
        self.assertEquals(data.values['test'], 10)
