# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import City


class CitiesListTestCase(TestCase):

    def setUp(self):
        super(CitiesListTestCase, self).setUp()

        city1 = City(state='AC', name='Test City 1')
        city2 = City(state='SP', name='Test City 2')

        db.session.add(city1)
        db.session.add(city2)

    @logged_as('admin', 'test')
    def test_cities_list(self):
        response = self.client.get(url_for('geo.cities_list'))
        self.assert200(response)

        cities = self.get_context_variable('cities')
        self.assertEquals(len(cities.items), 2)
