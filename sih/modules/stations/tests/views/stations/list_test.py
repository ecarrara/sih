# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.stations.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source


class StationsListTestCase(TestCase):

    def setUp(self):
        super(StationsListTestCase, self).setUp()

        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')

        station1 = Station(name='Test 1', code='test1',
                           kind=['pluviometric'], source=source,
                           location=WKTElement('POINT(-27 -45)'),
                           altitude=10)
        station2 = Station(name='Test 2', code='test2',
                           kind=['pluviometric', 'barrage'], source=source,
                           location=WKTElement('POINT(-27 -45)'),
                           altitude=10)
        station3 = Station(name='Test 3', code='test3',
                           kind=['quality'], source=source,
                           location=WKTElement('POINT(-27 -45)'),
                           altitude=10)

        db.session.add(station1)
        db.session.add(station2)
        db.session.add(station3)

    @logged_as('admin', 'test')
    def test_stations_list(self):
        url = url_for('stations.stations_list', kind='pluviometric')
        response = self.client.get(url)

        self.assert200(response)

        stations = self.get_context_variable('stations')

        self.assertEquals(len(stations.items), 2)
        self.assertEquals(stations.items[0].name, 'Test 1')
        self.assertEquals(stations.items[1].name, 'Test 2')
