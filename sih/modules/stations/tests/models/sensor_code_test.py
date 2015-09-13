# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.models.sensor_code_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.tests import TestCase
from sih.modules.stations.models import Sensor


class SensorCodeTestCase(TestCase):

    def test_validate_data(self):
        """Deve ser possível validar o dado do sensor usando um código
        embutido.
        """

        sensor = Sensor(name='Test', identifier='test', measure_unit='mm',
                        validate_code='result = value < 10')

        self.assertTrue(sensor.validate_data(5))
        self.assertFalse(sensor.validate_data(20))

    def test_process_data(self):
        """Deve ser possível processar um dado do sensor usando um código
        embutido.
        """

        sensor = Sensor(name='Test', identifier='test', measure_unit='mm',
                        process_code='result = value * 10')

        self.assertEquals(sensor.process_data(5), 50)

    def test_empty_process_code(self):
        """Não deve ser realizado processamento caso não haja uma rotina
        de processamento no sensor.
        """

        sensor = Sensor(name='Test', identifier='test', measure_unit='mm')
        self.assertEquals(sensor.process_data(5), 5)

    def test_empty_validate_code(self):
        """Todo valor deve ser considerado válido caso não haja uma rotina
        de vaildação no sensor.
        """

        sensor = Sensor(name='Test', identifier='test', measure_unit='mm')
        self.assertTrue(sensor.validate_data(-5))
