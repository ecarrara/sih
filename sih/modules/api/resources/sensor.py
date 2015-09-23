# -*- coding: utf-8 -*-
"""
    sih.modules.api.views.sensor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.modules.api.resources import ApiResource
from sih.modules.stations.models import Sensor


class SensorResource(ApiResource):

    model_class = Sensor
    model_id = 'identifier'
    page_size = 50
    schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
            'identifier': {
                'type': 'string',
                'pattern': '[-_a-z0-9]+'
            },
            'measure_unit': {
                'type': 'string',
            }
        },
        'additionalProperties': False,
        'required': ['name', 'identifier', 'measure_unit']
    }

    def short_representation(self, obj):
        return {
            'name': obj.name,
            'identifier': obj.identifier,
            'measure_unit': obj.measure_unit
        }

    def full_representation(self, obj):
        return self.short_representation(obj)

    def populate_object(self, obj, data):
        obj.name = data['name']
        obj.identifier = data['identifier']
        obj.measure_unit = data['measure_unit']
