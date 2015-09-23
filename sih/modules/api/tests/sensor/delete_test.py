# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.sensor.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.api.auth import basic_auth
from sih.modules.stations.models import Sensor


class ApiSensorsDeleteTestCase(TestCase):

    def setUp(self):
        super(ApiSensorsDeleteTestCase, self).setUp()

        sensor = Sensor(name='Test', identifier='test1', measure_unit='test')
        db.session.add(sensor)

    def test_api_stations_delete(self):
        url = url_for('api.sensors', obj_id='test1')

        response = self.client.delete(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Sensor.query.count(), 0)

    def test_api_stations_delete_not_found(self):
        url = url_for('api.sensors', obj_id='test-not-found')

        response = self.client.delete(url, headers={
            'Authorization': basic_auth('admin', 'secret'),
            'Content-Type': 'application/json'
        })

        self.assertEquals(response.status_code, 404)
