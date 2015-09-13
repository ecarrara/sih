# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sources.delete_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Source


class SourcesDeleteTestCase(TestCase):

    def setUp(self):
        super(SourcesDeleteTestCase, self).setUp()

        source = Source(id=1, name='Test 1', identifier='test1',
                        url='http://example.com/1')
        db.session.add(source)

        self.url = url_for('stations.sources_delete', source_id=source.id)

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem excluír fontes de
        dados.
        """

        response = self.client.post(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_delete_source(self):
        """Deve ser possível excluír uma fonte de dados.
        """

        response = self.client.post(self.url)
        self.assertRedirects(response, url_for('stations.sources_list'))

        self.assertEquals(Source.query.count(), 0)
