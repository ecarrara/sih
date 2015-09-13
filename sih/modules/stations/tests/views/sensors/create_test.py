# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sensors.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.modules.stations.models import Sensor


class SensorsCreateTestCase(TestCase):

    def setUp(self):
        super(SensorsCreateTestCase, self).setUp()

        self.url = url_for('stations.sensors_create')

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem cadastrar sensores.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_render_create_sensor_page(self):
        """Deve ser possível visualizar a página de cadastro de sensor.
        """

        response = self.client.get(self.url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_create_sensor(self):
        """Deve ser possível criar um sensor.
        """

        response = self.client.post(self.url, data={
            'name': 'Test',
            'identifier': 'test',
            'measure_unit': 'mm'
        })

        self.assertRedirects(response, url_for('stations.sensors_list'))

        sensor = Sensor.query.filter(Sensor.identifier == 'test').first()
        self.assertIsNotNone(sensor)

    @logged_as('admin', 'test')
    def test_invalid_validate_and_process_code(self):
        """Não deve ser possível cadastrar um sensor com código de validação
        e/ou código de processamento inválido.
        """

        response = self.client.post(self.url, data={
            'name': 'Test',
            'identifier': 'test',
            'license': 'Public domain',
            'url': 'h:/example@com',
            'process_code': 'result = value @ 10',
            'validate_code': '__result = invalid'
        })

        self.assert200(response)

        form = self.get_context_variable('form')

        self.assertTrue(form.errors['process_code'])
        self.assertTrue(form.errors['validate_code'])

        self.assertEquals(Sensor.query.count(), 0)
