# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.basins.view_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import Basin


class BasinsViewTestCase(TestCase):

    def setUp(self):
        super(BasinsViewTestCase, self).setUp()

        basin = Basin(ottocode='1',
                      boundary=WKTElement('POLYGON ((1 1, 2 1, 1 2, 1 1))'))

        db.session.add(basin)

    @logged_as('admin', 'test')
    def test_view_basin(self):
        response = self.client.get(url_for('geo.basins_view', basin_id='1'))
        self.assert200(response)
