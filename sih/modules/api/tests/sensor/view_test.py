# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.sensor.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Sensor


class ApiSensorsListTestCase(TestCase):

    def setUp(self):
        super(ApiSensorsListTestCase, self).setUp()

        sensor = Sensor(name='Test 1', identifier='test1', measure_unit='mm')

        db.session.add(sensor)

    def test_api_sensors_list(self):
        url = url_for('api.sensors', obj_id='test1')

        response = self.client.get(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assert200(response)
