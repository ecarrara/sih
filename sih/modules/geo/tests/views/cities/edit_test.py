# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import City


class CitiesEditTestCase(TestCase):

    def setUp(self):
        super(CitiesEditTestCase, self).setUp()
        city = City(id=1, state='AC', name='Test City 1')
        db.session.add(city)

    @logged_as('admin', 'test')
    def test_render_edit_city_page(self):
        url = url_for('geo.cities_edit', city_id=1)
        response = self.client.get(url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_edit_city(self):
        url = url_for('geo.cities_edit', city_id=1)
        response = self.client.post(url, data={
            'id': '2',
            'name': 'Test Modified',
            'state': 'SP'
        })

        self.assertRedirects(response, url_for('geo.cities_view', city_id=2))

        city = City.query.filter(City.id == 2).first()
        self.assertEquals(city.name, 'Test Modified')
        self.assertEquals(city.state, 'SP')
