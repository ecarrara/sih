# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sources.list_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db, login_manager
from sih.modules.stations.models import Source


class SourcesListTestCase(TestCase):

    def setUp(self):
        super(SourcesListTestCase, self).setUp()

        self.url = url_for('stations.sources_list')

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem visualizar a
        lista de fontes de dados.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_list_sensors(self):
        """Deve ser possível visualizar a lista de fontes de dados.
        """

        db.session.add(Source(name='Test 1', identifier='test1',
                              url='http://example.com/1'))
        db.session.add(Source(name='Test 2', identifier='test2',
                              url='http://example.com/2'))

        response = self.client.get(self.url)
        self.assert200(response)

        sources = self.get_context_variable('sources')
        self.assertEquals(len(sources), 2)
