# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.stations.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source


class StationsEditTestCase(TestCase):

    def setUp(self):
        super(StationsEditTestCase, self).setUp()

        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')
        station = Station(name='Test', code='test',
                          kind=['pluviometric'], source=source,
                          altitude=10)

        db.session.add(station)
        db.session.commit()

        self.url = url_for('stations.stations_edit', station_id=station.id)

    def test_permission_required(self):
        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_render_form(self):
        response = self.client.get(self.url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_valid_station_information(self):
        response = self.client.post(self.url, data={
            'name': u'Modified',
            'source': u'1',
            'code': 'test',
            'kind': 'pluviometric, quality',
            'installed_at': '28/11/2015',
            'interval': '15',
            'description': ''
        })

        url = url_for('stations.stations_view', station_id=1)
        self.assertRedirects(response, url)

        station = Station.query.filter(Station.name == 'Modified').first()
        self.assertIsNotNone(station)
