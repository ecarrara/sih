# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sensors.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Sensor


class SensorsDeleteTestCase(TestCase):

    def setUp(self):
        super(SensorsDeleteTestCase, self).setUp()

        sensor = Sensor(id=1, name='Test 1', identifier='test1',
                        measure_unit='mm')
        db.session.add(sensor)

        self.url = url_for('stations.sensors_delete', sensor_id=sensor.id)

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem excluír sensores.
        """

        response = self.client.post(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_delete_sensor(self):
        """Deve ser possível excluír um sensor.
        """

        response = self.client.post(self.url)
        self.assertRedirects(response, url_for('stations.sensors_list'))

        self.assertEquals(Sensor.query.count(), 0)
