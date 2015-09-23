# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.sensor.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Sensor


class ApiSensorsCreateTestCase(TestCase):

    def test_api_sensor_create(self):
        url = url_for('api.sensors')

        response = self.client.post(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'name': 'Test',
            'identifier': 'test',
            'measure_unit': 'mm'
        }))

        self.assertEquals(response.status_code, 201)

        sensor = Sensor.query.filter(Sensor.identifier == 'test').first()
        self.assertIsNotNone(sensor)
        self.assertEquals(sensor.name, 'Test')
        self.assertEquals(sensor.measure_unit, 'mm')
