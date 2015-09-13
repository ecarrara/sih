# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sensors.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Sensor


class SensorsEditTestCase(TestCase):

    def setUp(self):
        super(SensorsEditTestCase, self).setUp()

        sensor = Sensor(id=1, name='Test 1', identifier='test1',
                        measure_unit='mm')
        db.session.add(sensor)

        self.url = url_for('stations.sensors_edit', sensor_id=sensor.id)

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem editar sensores.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_render_edit_sensor_page(self):
        """Deve ser possível visualizar a página de edição de sensor.
        """

        response = self.client.get(self.url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_edit_sensor(self):
        """Deve ser possível editar uma sensor.
        """

        response = self.client.post(self.url, data={
            'name': 'Test',
            'identifier': 'modified',
            'measure_unit': 'mm'
        })

        self.assertRedirects(response, url_for('stations.sensors_list'))

        sensor = Sensor.query.filter(Sensor.identifier == 'modified').first()
        self.assertIsNotNone(sensor)
        self.assertEquals(Sensor.query.count(), 1)
