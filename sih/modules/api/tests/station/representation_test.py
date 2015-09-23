# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.stations.representation_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase
from sih.modules.api.resources.station import StationResource
from sih.modules.stations.models import Station, Source, Sensor


class ApiStationsRepresentationTestCase(TestCase):

    def setUp(self):
        super(ApiStationsRepresentationTestCase, self).setUp()

        self.station = Station(name='Test 1', code='test1',
                               kind=['pluviometric'],
                               created_at=datetime(1994, 1, 6, 12, 0, 0),
                               installed_at=datetime(1994, 10, 27, 20, 0, 0),
                               source=Source(name='Test 1',
                                             identifier='test-source1',
                                             url='http://example.com',
                                             license='OpenData'),
                               sensors=[Sensor(name='Rainfall',
                                               identifier='rainfall',
                                               measure_unit='mm/h')],
                               location=WKTElement('POINT (2 1)'),
                               altitude=100)

        self.resource = StationResource()

    def test_full_representation(self):
        representation = self.resource.full_representation(self.station)

        self.assertEquals(representation, {
            'code': 'test1',
            'name': 'Test 1',
            'created_at': datetime(1994, 1, 6, 12, 0, 0),
            'installed_at': datetime(1994, 10, 27, 20, 0, 0),
            'kind': ['pluviometric'],
            'description': None,
            'source': {
                'name': 'Test 1',
                'identifier': 'test-source1',
                'url': 'http://example.com',
                'license': 'OpenData'
            },
            'location': [2.0, 1.0],
            'altitude': 100,
            'interval': None,
            'sensors': [{
                'name': 'Rainfall',
                'identifier': 'rainfall',
                'measure_unit': 'mm/h',
            }]
        })

    def test_short_representation(self):
        representation = self.resource.short_representation(self.station)

        self.assertEquals(representation, {
            'code': 'test1',
            'name': 'Test 1',
            'kind': ['pluviometric'],
            'source': 'test-source1',
            'sensors': ['rainfall'],
            'location': [2.0, 1.0],
        })
