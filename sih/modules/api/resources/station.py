# -*- coding: utf-8 -*-
"""
    sih.modules.api.views.stations
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

import jsonschema
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import String
from sih.modules.api.resources import ApiResource
from sih.modules.api.exceptions import ApiError
from sih.modules.stations.models import Station, Source, Sensor, StationSensor


class StationResource(ApiResource):

    model_class = Station
    model_id = 'code'
    page_size = 1
    schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
            'code': {
                'type': 'string',
                'pattern': '[-_a-z0-9]+'
            },
            'installed_at': {
                'type': 'string',
                'format': 'date-time'
            },
            'kind': {
                'type': 'array',
                'items': {
                    'type': 'string'
                },
                'minItems': 1
            },
            'source': {
                'type': 'string'
            },
            'sensors': {
                'type': 'array',
                'items': {
                    'type': 'string'
                },
                'minItems': 1,
                'uniqueItems': True
            },
            'location': {
                'type': 'array',
                'items': {
                    'type': 'number'
                },
                'minItems': 2,
                'maxItems': 2
            },
            'altitude': {
                'type': 'integer'
            }
        },
        'additionalProperties': False,
        'required': ['name', 'code', 'kind', 'source', 'sensors']
    }

    def validate_data(self, data):
        try:
            jsonschema.validate(data, self.schema,
                                format_checker=jsonschema.FormatChecker())
        except jsonschema.ValidationError as e:
            raise ApiError(e.message, 400)

    def apply_filters(self, query, filters):
        source = filters.get('source')
        kind = filters.get('kind')
        sensor = filters.get('sensor')
        bbox = filters.get('bbox')

        if source:
            source = source.split(',')
            query = query.join(Source, Station.source_id == Source.id) \
                         .filter(Source.identifier.in_(source))

        if kind:
            kind = kind.split(',')
            query = query.filter(
                Station.kind.overlap(cast(kind, ARRAY(String)))
            )

        if sensor:
            sensor = sensor.split(',')
            query = query.join(StationSensor,
                               StationSensor.station_id == Station.id) \
                         .join(Sensor,
                               StationSensor.sensor_id == Sensor.id) \
                         .filter(Sensor.identifier.in_(sensor))

        if bbox:
            try:
                left, bottom, right, top = map(float, bbox.split(','))
            except ValueError:
                raise ApiError(u'Invalid bbox', 400)

            bbox = 'POLYGON(({l} {b}, {r} {b}, {r} {t}, {l} {t}, {l} {b}))' \
                   .format(l=left, b=bottom, r=right, t=top)

            query = query.filter(Station.location.ST_CoveredBy(bbox))

        return query

    def short_representation(self, obj):
        return {
            'code': obj.code,
            'name': obj.name,
            'kind': obj.kind,
            'location': [obj.latlng.x, obj.latlng.y] if obj.latlng else None,
            'source': obj.source.identifier,
            'sensors': [sensor.identifier for sensor in obj.sensors]
        }

    def full_representation(self, obj):
        return {
            'code': obj.code,
            'name': obj.name,
            'created_at': obj.created_at,
            'installed_at': obj.installed_at,
            'kind': obj.kind,
            'description': obj.description,
            'source': {
                'name': obj.source.name,
                'identifier': obj.source.identifier,
                'url': obj.source.url,
                'license': obj.source.license
            },
            'location': [obj.latlng.x, obj.latlng.y] if obj.latlng else None,
            'altitude': obj.altitude,
            'interval': obj.interval,
            'sensors': [{
                'name': sensor.name,
                'identifier': sensor.identifier,
                'measure_unit': sensor.measure_unit
            } for sensor in obj.sensors]
        }

    def populate_object(self, station, data):
        source = Source.query \
                       .filter(Source.identifier == data['source']) \
                       .first()
        if source is None:
            raise ApiError(u'Source {} not exists'.format(data['source']), 400)

        station.name = data['name']
        station.code = data['code']
        station.kind = data['kind']
        station.installed_at = data.get('installed_at')
        station.altitude = data.get('altitude')
        station.source = source

        if data.get('location'):
            station.location = \
                'POINT({lng} {lat})'.format(lat=data['location'][0],
                                            lng=data['location'][1])

        station.sensors = []
        for sensor_id in data['sensors']:
            sensor = Sensor.query \
                           .filter(Sensor.identifier == sensor_id) \
                           .first()
            if sensor is None:
                raise ApiError(u'Sensor {} not exists'.format(sensor_id), 400)

            station.sensors.append(sensor)
