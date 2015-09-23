# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.stations.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Station, Source, Sensor


class ApiStationsListTestCase(TestCase):

    def setUp(self):
        super(ApiStationsListTestCase, self).setUp()

        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')

        station1 = Station(name='Test 1', code='test1',
                           kind=['pluviometric'], source=source,
                           sensors=[Sensor(name='Test', identifier='test',
                                           measure_unit='test')],
                           location=WKTElement('POINT(1 1)'))
        station2 = Station(name='Test 2', code='test2',
                           kind=['pluviometric', 'barrage'],
                           source=source)
        station3 = Station(name='Test 3', code='test3',
                           kind=['quality'],
                           source=source)

        db.session.add(station1)
        db.session.add(station2)
        db.session.add(station3)

    def test_api_stations_list(self):
        url = url_for('api.stations')
        response = self.client.get(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)

        data = response.json
        self.assertEquals(len(data['data']), 3)

    def test_api_stations_filters(self):
        url = url_for('api.stations')

        response = self.client.get(url, query_string={
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
        self.assertEquals(data['data'][0]['code'], 'test1')

    def test_api_stations_invalid_bbox(self):
        url = url_for('api.stations')

        response = self.client.get(url, query_string={
            'bbox': '0,a,2,b'
        }, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assertEquals(response.status_code, 400)
