# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import City


class CitiesDeleteTestCase(TestCase):

    def setUp(self):
        super(CitiesDeleteTestCase, self).setUp()

        city = City(id=1, state='AC', name='Test City 1',
                    boundary=WKTElement('POLYGON ((0 0, 1 1, 1 2, 0 0))'))

        db.session.add(city)

    @logged_as('admin', 'test')
    def test_delete_city(self):
        response = self.client.post(url_for('geo.cities_delete', city_id=1))
        self.assertRedirects(response, url_for('geo.cities_list'))
        self.assertEquals(City.query.count(), 0)
