# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.data.representation_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase
from sih.modules.api.resources.data import DataResource
from sih.modules.stations.models import Station, Source, Sensor
from sih.modules.data.models import Data, SensorData


class ApiDataRepresentationTestCase(TestCase):

    def setUp(self):
        super(ApiDataRepresentationTestCase, self).setUp()

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

        self.data = Data(id=1,
                         station=station,
                         read_at=datetime(1994, 10, 27, 8),
                         sensor_data=[SensorData(sensor=sensor, value=2)])

        self.resource = DataResource()

    def test_full_representation(self):
        full_representation = self.resource.full_representation(self.data)

        self.maxDiff = None
        self.assertEquals(full_representation, {
            'id': 1,
            'read_at': datetime(1994, 10, 27, 8),
            'values': {
                'test': 2
            },
            'station': {
                'code': 'test1',
                'name': 'Test 1',
                'kind': ['pluviometric'],
                'location': [-27.0, -45.0],
                'altitude': 10,
                'interval': None,
                'sensors': [{
                    'name': 'Test',
                    'identifier': 'test',
                    'measure_unit': 'mm'
                }],
                'source': {
                    'name': 'Test 1',
                    'identifier': 'test1',
                    'url': 'http://example.com',
                    'license': 'OpenData'
                }
            }
        })

    def test_short_representation(self):
        short_representation = self.resource.short_representation(self.data)

        self.assertEquals(short_representation, {
            'id': 1,
            'read_at': datetime(1994, 10, 27, 8),
            'values': {
                'test': 2
            },
            'station': {
                'code': 'test1',
                'name': 'Test 1',
                'kind': ['pluviometric'],
                'location': [-27.0, -45.0],
                'altitude': 10,
                'source': 'test1'
            }
        })
