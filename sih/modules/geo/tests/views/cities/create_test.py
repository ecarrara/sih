# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase, logged_as
from sih.modules.geo.models import City


class CitiesCreateTestCase(TestCase):

    @logged_as('admin', 'test')
    def test_render_create_city_page(self):
        response = self.client.get(url_for('geo.cities_create'))
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_create_city(self):
        response = self.client.post(url_for('geo.cities_create'), data={
            'id': '2',
            'name': 'Test Modified',
            'state': 'SP',
            'boundary': json.dumps({
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [[1, 2], [2, 2], [1, 2]]
                        ]
                    }
                }]
            })
        })

        self.assertRedirects(response, url_for('geo.cities_view', city_id=2))

        city = City.query.filter(City.id == 2).first()
        self.assertEquals(city.name, 'Test Modified')
        self.assertEquals(city.state, 'SP')
