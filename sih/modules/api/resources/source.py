# -*- coding: utf-8 -*-
"""
    sih.modules.api.resources.source
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

import jsonschema
from sih.modules.api.resources import ApiResource
from sih.modules.api.exceptions import ApiError
from sih.modules.stations.models import Source


class SourceResource(ApiResource):

    model_class = Source
    model_id = 'identifier'
    page_size = 50
    schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string'
            },
            'identifier': {
                'type': 'string',
                'pattern': '[-_a-z0-9]+'
            },
            'measure_unit': {
                'type': 'string'
            },
            'url': {
                'type': 'string'
            },
            'license': {
                'type': 'string'
            }
        },
        'additionalProperties': False,
        'required': ['name', 'identifier']
    }

    def validate_data(self, data):
        try:
            jsonschema.validate(data, self.schema,
                                format_checker=jsonschema.FormatChecker())
        except jsonschema.ValidationError as e:
            raise ApiError(e.message, 400)

    def short_representation(self, obj):
        return {
            'name': obj.name,
            'identifier': obj.identifier,
            'url': obj.url,
            'license': obj.license
        }

    def full_representation(self, obj):
        return self.short_representation(obj)

    def populate_object(self, obj, data):
        obj.name = data['name']
        obj.identifier = data['identifier']
        obj.url = data['url']
        obj.license = data['license']
