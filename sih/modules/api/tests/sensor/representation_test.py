# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.sensor.representation_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.tests import TestCase
from sih.modules.api.resources.sensor import SensorResource
from sih.modules.stations.models import Sensor


class ApiSensorsRepresentationTestCase(TestCase):

    def setUp(self):
        super(ApiSensorsRepresentationTestCase, self).setUp()

        self.sensor = Sensor(name='Rainfall',
                             identifier='rainfall',
                             measure_unit='mm')

        self.resource = SensorResource()

    def test_full_representation(self):
        full_representation = self.resource.full_representation(self.sensor)

        self.assertEquals(full_representation, {
            'identifier': 'rainfall',
            'name': 'Rainfall',
            'measure_unit': 'mm'
        })

    def test_short_representation(self):
        short_representation = self.resource.short_representation(self.sensor)

        self.assertEquals(short_representation, {
            'identifier': 'rainfall',
            'name': 'Rainfall',
            'measure_unit': 'mm'
        })
