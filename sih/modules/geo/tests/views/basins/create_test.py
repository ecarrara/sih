# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.basins.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for, json
from sih.tests import TestCase, logged_as
from sih.modules.geo.models import Basin


class BasinsCreateTestCase(TestCase):

    @logged_as('admin', 'test')
    def test_render_create_basin_page(self):
        response = self.client.get(url_for('geo.basins_create'))
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_create_basin(self):
        response = self.client.post(url_for('geo.basins_create'), data={
            'ottocode': '5935',
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

        self.assertRedirects(response,
                             url_for('geo.basins_view', basin_id=5935))

        basin = Basin.query.filter(Basin.ottocode == '5935').first()
        self.assertIsNotNone(basin)
