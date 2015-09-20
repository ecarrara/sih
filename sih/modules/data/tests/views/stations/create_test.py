# -*- coding: utf-8 -*-
"""
    sih.modules.data.tests.views.stations.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source, Sensor
from sih.modules.data.models import Data


class CreateStationDataTestCase(TestCase):

    def setUp(self):
        super(CreateStationDataTestCase, self).setUp()

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

        db.session.add(station)

    def test_permission_required(self):
        url = url_for('data.stations_create', station_id=1)
        response = self.client.post(url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_create_station_data(self):
        url = url_for('data.stations_create', station_id=1)

        response = self.client.post(url, data={
            'station': 1,
            'read_at': '2012-10-27T08:00',
            'sensor_data-0-sensor': 1,
            'sensor_data-0-value': 2
        })

        self.assertRedirects(response,
                             url_for('data.stations_view', station_id=1))
        self.assertEquals(Data.query.count(), 1)

        data = Data.query.filter(Data.station_id == 1).first()
        self.assertEquals(data.values['test'], 4)

    @logged_as('admin', 'test')
    def test_create_station_data_invalid_sensor_value(self):
        url = url_for('data.stations_create', station_id=1)

        response = self.client.post(url, data={
            'station': 1,
            'read_at': '2012-10-27T08:00',
            'sensor_data-0-sensor': 1,
            'sensor_data-0-value': -1
        })

        self.assert200(response)

        form = self.get_context_variable('form')
        self.assertTrue(form.sensor_data.errors)

        self.assertEquals(Data.query.count(), 0)

    @logged_as('admin', 'test')
    def test_create_station_data_non_numeric_sensor_value(self):
        url = url_for('data.stations_create', station_id=1)

        response = self.client.post(url, data={
            'station': 1,
            'read_at': '2012-10-27T08:00',
            'sensor_data-0-sensor': 1,
            'sensor_data-0-value': 'avocade'
        })

        self.assert200(response)

        form = self.get_context_variable('form')
        self.assertTrue(form.sensor_data.errors)

        self.assertEquals(Data.query.count(), 0)

    @logged_as('admin', 'test')
    def test_create_station_data_future_read_at(self):
        url = url_for('data.stations_create', station_id=1)

        response = self.client.post(url, data={
            'station': 1,
            'read_at': '2100-10-27T08:00',  # happy birthday Lu (106 years old)
            'sensor_data-0-sensor': 1,
            'sensor_data-0-value': 'avocade'
        })

        self.assert200(response)

        form = self.get_context_variable('form')
        self.assertTrue(form.sensor_data.errors)

        self.assertEquals(Data.query.count(), 0)
