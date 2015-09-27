# -*- coding: utf-8 -*-
"""
    sih.modules.geo.tests.views.basins.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.geo.models import Basin


class BasinsListTestCase(TestCase):

    def setUp(self):
        super(BasinsListTestCase, self).setUp()

        basin1 = Basin(ottocode='1',
                       boundary=WKTElement('POLYGON ((0 0, 1 1, 1 2, 0 0))'))
        basin2 = Basin(ottocode='2',
                       boundary=WKTElement('POLYGON ((1 1, 2 2, 3 4, 1 1))'))

        db.session.add(basin1)
        db.session.add(basin2)

    @logged_as('admin', 'test')
    def test_basins_list(self):
        response = self.client.get(url_for('geo.basins_list'))
        self.assert200(response)

        basins = self.get_context_variable('basins')
        self.assertEquals(len(basins), 2)
