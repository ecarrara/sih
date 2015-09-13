# -*- coding: utf-8 -*-
"""
    sih.modules.stations.tests.views.sources.create_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""


from flask import url_for
from sih.tests import TestCase, logged_as
from sih.modules.stations.models import Source


class SourcesCreateTestCase(TestCase):

    def setUp(self):
        super(SourcesCreateTestCase, self).setUp()

        self.url = url_for('stations.sources_create')

    def test_admin_permission_required(self):
        """Apenas usuários com papel de *admin* podem cadastrar fontes de
        dados.
        """

        response = self.client.get(self.url)
        self.assert403(response)

    @logged_as('admin', 'test')
    def test_render_create_source_page(self):
        """Deve ser possível visualizar a página de cadastro de fonte de dados.
        """

        response = self.client.get(self.url)
        self.assert200(response)

    @logged_as('admin', 'test')
    def test_create_source(self):
        """Deve ser possível criar uma fonte de dados.
        """

        response = self.client.post(self.url, data={
            'name': 'Test',
            'identifier': 'test',
            'license': 'Public domain',
            'url': 'http://example.com'
        })

        self.assertRedirects(response, url_for('stations.sources_list'))

        source = Source.query.filter(Source.identifier == 'test').first()
        self.assertEquals(source.name, 'Test')
        self.assertEquals(source.license, 'Public domain')
        self.assertEquals(source.url, 'http://example.com')

    @logged_as('admin', 'test')
    def test_invalid_url(self):
        """Deve ser possível criar uma fonte de dados com uma URL inválida.
        """

        response = self.client.post(self.url, data={
            'name': 'Test',
            'identifier': 'test',
            'license': 'Public domain',
            'url': 'h:/example@com'
        })

        self.assert200(response)
        self.assertEquals(Source.query.count(), 0)
