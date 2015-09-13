# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sensors.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Sensor


class SensorsListTestCase(TestCase):

    def setUp(self):
        super(SensorsListTestCase, self).setUp()

        self.url = url_for('stations.sensors_list')

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem visualizar a
        lista de sensores.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_list_sensors(self):
        """Deve ser possível visualizar a lista de sensores.
        """

        db.session.add(Sensor(name='Test 1', identifier='test1',
                              measure_unit='mm'))
        db.session.add(Sensor(name='Test 2', identifier='test2',
                              measure_unit='mm'))

        response = self.client.get(self.url)
        self.assert200(response)

        sensors = self.get_context_variable('sensors')
        self.assertEquals(len(sensors), 2)
