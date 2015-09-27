# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.basins.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import Basin


class BasinsDeleteTestCase(TestCase):

    def setUp(self):
        super(BasinsDeleteTestCase, self).setUp()

        basin = Basin(ottocode='1',
                      boundary=WKTElement('POLYGON ((0 0, 1 1, 1 2, 0 0))'))

        db.session.add(basin)

    @logged_as('admin', 'test')
    def test_delete_basin(self):
        response = self.client.post(url_for('geo.basins_delete', basin_id=1))
        self.assertRedirects(response, url_for('geo.basins_list'))
        self.assertEquals(Basin.query.count(), 0)
