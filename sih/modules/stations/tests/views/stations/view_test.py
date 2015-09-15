# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.stations.view_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source


class StationsViewTestCase(TestCase):

    def test_permission_required(self):
        url = url_for('stations.stations_view', station_id=1)
        response = self.client.get(url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_station_not_found(self):
        url = url_for('stations.stations_view', station_id=1)
        response = self.client.get(url)
        self.assert404(response)

    @logged_as('admin', 'test')
    def test_station_view(self):
        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')

        station = Station(name='Test 1', code='test1',
                          kind=['pluviometric'], source=source,
                          location=WKTElement('POINT(-27 -45)'),
                          altitude=10)
        db.session.add(station)

        url = url_for('stations.stations_view', station_id=1)
        response = self.client.get(url)

        self.assert200(response)
