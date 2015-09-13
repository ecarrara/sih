# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sources.view_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Source


class SourcesViewTestCase(TestCase):

    def setUp(self):
        super(SourcesViewTestCase, self).setUp()

        source = Source(id=1, name='Test 1', identifier='test1',
                        url='http://example.com/1')
        db.session.add(source)

        self.url = url_for('stations.sources_view', source_id=source.id)

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem visualizar fontes de
        dados.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_view_source(self):
        """Deve ser possível visualizar uma fonte de dados.
        """

        response = self.client.get(self.url)
        self.assert200(response)
