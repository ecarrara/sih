# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sensors.view_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Sensor


class SensorsViewTestCase(TestCase):

    def setUp(self):
        super(SensorsViewTestCase, self).setUp()

        sensor = Sensor(id=1, name='Test 1', identifier='test1',
                        measure_unit='mm')
        db.session.add(sensor)

        self.url = url_for('stations.sensors_view', sensor_id=sensor.id)

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem visualizar sensores.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_view_sensor(self):
        """Deve ser possível visualizar uma sensor.
        """

        response = self.client.get(self.url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_validate_and_process_code(self):
        """Deve ser possível testar os códigos de validação e processamento.
        """

        sensor = Sensor(id=100, name='Test 100', identifier='test100',
                        measure_unit='mm/h',
                        process_code='result = value * 2',
                        validate_code='result = value < 100')
        db.session.add(sensor)

        url = url_for('stations.sensors_view', sensor_id=100)
        response = self.client.post(url, data={
            'input': '4'
        })

        self.assert200(response)

        process_output = self.get_context_variable('process_output')
        validate_output = self.get_context_variable('validate_output')

        self.assertEquals(process_output, 8)
        self.assertTrue(validate_output)

    @logged_as('admin', 'test')
    def test_invalid_process_and_output_code(self):
        """Deve ser tratado código de processamento e validação inválidos.
        """

        sensor = Sensor(id=101, name='Test 101', identifier='test101',
                        measure_unit='mm/h',
                        process_code='result = value !> 2',
                        validate_code='result = value ( 100')
        db.session.add(sensor)

        url = url_for('stations.sensors_view', sensor_id=101)
        response = self.client.post(url, data={
            'input': '4'
        })

        self.assert200(response)

        process_error = self.get_context_variable('process_error')
        validate_error = self.get_context_variable('validate_error')

        self.assertIsNotNone(process_error)
        self.assertIsNotNone(validate_error)
