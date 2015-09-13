# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.view_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import City


class CitiesViewTestCase(TestCase):

    def setUp(self):
        super(CitiesViewTestCase, self).setUp()

        city = City(id=1, state='AC', name='Test City 1',
                    boundary=WKTElement('POLYGON ((0 0, 1 1, 1 2, 0 0))'))

        db.session.add(city)

    @logged_as('admin', 'test')
    def test_view_city(self):
        response = self.client.get(url_for('geo.cities_view', city_id=1))
        self.assert200(response)
