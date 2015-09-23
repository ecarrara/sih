# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.sensor.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Sensor


class ApiSensorsEditTestCase(TestCase):

    def test_api_sensor_edit(self):
        sensor = Sensor(name='Test', identifier='test', measure_unit='mm')
        db.session.add(sensor)

        url = url_for('api.sensors', obj_id='test')

        response = self.client.put(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'name': 'Test Modified',
            'identifier': 'modified',
            'measure_unit': 'm'
        }))

        self.assertEquals(response.status_code, 200)

        sensor = Sensor.query.filter(Sensor.identifier == 'modified').first()
        self.assertIsNotNone(sensor)
        self.assertEquals(sensor.name, 'Test Modified')
        self.assertEquals(sensor.measure_unit, 'm')
