# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sources.edit_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from sih.tests import TestCase, logged_as
from sih.extensions import db
from sih.modules.stations.models import Source


class SourcesEditTestCase(TestCase):

    def setUp(self):
        super(SourcesEditTestCase, self).setUp()

        source = Source(id=1, name='Test 1', identifier='test1',
                        url='http://example.com/1')
        db.session.add(source)

        self.url = url_for('stations.sources_edit', source_id=source.id)

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem editar fontes de
        dados.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_render_edit_source_page(self):
        """Deve ser possível visualizar a página de edição de fonte de dados.
        """

        response = self.client.get(self.url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_edit_source(self):
        """Deve ser possível editar uma fonte de dados.
        """

        response = self.client.post(self.url, data={
            'name': 'Test',
            'identifier': 'modified',
            'license': 'Public domain',
            'url': 'http://example.com'
        })

        self.assertRedirects(response, url_for('stations.sources_list'))

        source = Source.query.filter(Source.identifier == 'modified').first()
        self.assertIsNotNone(source)
        self.assertEquals(Source.query.count(), 1)
