# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.stations.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from geoalchemy2.elements import WKTElement
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Station, Source


class StationsCreateTestCase(TestCase):

    def setUp(self):
        super(StationsCreateTestCase, self).setUp()
        self.source = Source(name='Test 1', identifier='test1',
                             url='http://example.com', license='OpenData')

        db.session.add(self.source)
        db.session.commit()

        self.url = url_for('stations.stations_create')

    @logged_as('admin', 'test')
    def test_render_create_page(self):
        response = self.client.get(self.url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_valid_station_information(self):
        response = self.client.post(self.url, data={
            'name': u'Test',
            'source': u'1',
            'code': 'test',
            'kind': 'pluviometric, quality',
            'installed_at': '28/11/2015',
            'interval': '15',
            'description': ''
        })

        url = url_for('stations.stations_view', station_id=1)
        self.assertRedirects(response, url)
        self.assertTrue(Station.query.count(), 1)

    @logged_as('admin', 'test')
    def test_code_already_exists(self):
        station = Station(name='Test', code='test',
                          kind=['pluviometric'], source=self.source,
                          location=WKTElement('POINT(-27 -45)'),
                          altitude=10)
        db.session.add(station)

        response = self.client.post(self.url, data={
            'name': u'Test',
            'source': u'1',
            'code': 'test',
            'kind': 'pluviometric, quality',
            'installed_at': '28/11/2015',
            'interval': '15',
            'description': ''
        })

        self.assert200(response)

        form = self.get_context_variable('form')
        self.assertEquals(len(form.errors['code']), 1)
