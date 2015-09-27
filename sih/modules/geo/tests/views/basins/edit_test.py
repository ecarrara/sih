# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.basins.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import Basin


class BasinsEditTestCase(TestCase):

    def setUp(self):
        super(BasinsEditTestCase, self).setUp()
        basin = Basin(ottocode='1',
                      boundary=WKTElement('POLYGON ((0 0, 1 1, 1 2, 0 0))'))
        db.session.add(basin)

    @logged_as('admin', 'test')
    def test_render_edit_basin_page(self):
        url = url_for('geo.basins_edit', basin_id='1')
        response = self.client.get(url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_edit_basin(self):
        url = url_for('geo.basins_edit', basin_id='1')
        response = self.client.post(url, data={
            'ottocode': '2',
        })

        self.assertRedirects(response,
                             url_for('geo.basins_view', basin_id='2'))

        basin = Basin.query.filter(Basin.ottocode == '2').first()
        self.assertIsNotNone(basin)
