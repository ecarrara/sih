# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.stations.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source


class StationsDeleteTestCase(TestCase):

    def test_permission_required(self):
        response = self.client.post(url_for('stations.stations_delete',
                                            station_id=1))
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_station_not_found(self):
        response = self.client.post(url_for('stations.stations_delete',
                                            station_id=1))
        self.assert404(response)

    @logged_as('admin', 'test')
    def test_delete_station(self):
        source = Source(name='Test 1', identifier='test1',
                        url='http://example.com', license='OpenData')

        station = Station(id=1, name='Test 1', code='test1',
                          kind=['pluviometric'], source=source,
                          altitude=10)
        db.session.add(station)

        url = url_for('stations.stations_delete', station_id=1)
        response = self.client.post(url)

        self.assertRedirects(response, url_for('stations.stations_list'))
        self.assertEqual(Station.query.count(), 0)
