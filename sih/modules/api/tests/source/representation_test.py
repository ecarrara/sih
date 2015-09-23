# -*- coding: utf-8 -*-
"""
    sih.modules.api.tests.source.representation_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.tests import TestCase
from sih.modules.api.resources.source import SourceResource
from sih.modules.stations.models import Source


class ApiSourcesRepresentationTestCase(TestCase):

    def setUp(self):
        super(ApiSourcesRepresentationTestCase, self).setUp()

        self.source = Source(name='Example',
                             identifier='example',
                             license='OpenData',
                             url='http://example.com')

        self.resource = SourceResource()

    def test_full_representation(self):
        full_representation = self.resource.full_representation(self.source)

        self.assertEquals(full_representation, {
            'identifier': 'example',
            'name': 'Example',
            'license': 'OpenData',
            'url': 'http://example.com'
        })

    def test_short_representation(self):
        short_representation = self.resource.short_representation(self.source)

        self.assertEquals(short_representation, {
            'identifier': 'example',
            'name': 'Example',
            'license': 'OpenData',
            'url': 'http://example.com'
        })
