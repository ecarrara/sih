# -*- coding: utf-8 -*-
"""
    sih.modules.api.resources.data
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

import ciso8601
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import String
from sih.modules.api.exceptions import ApiError
from sih.modules.api.resources import ApiResource
from sih.modules.stations.models import Station, Source, Sensor, StationSensor
from sih.modules.data.models import Data, SensorData


class DataResource(ApiResource):

    model_class = Data
    model_id = 'id'
    limit = 500
    schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            'station': {
                'type': 'string',
                'pattern': '[-_a-z0-9]+'
            },
            'read_at': {
                'type': 'string',
                'format': 'date-time'
            },
            'values': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'sensor': {
                            'type': 'string',
                            'pattern': '[-_a-z0-9]+'
                        },
                        'value': {
                            'type': 'integer'
                        }
                    },
                    'required': ['sensor', 'value']
                }
            }
        },
        'additionalProperties': False,
        'required': ['read_at', 'station', 'values']
    }

    def short_representation(self, obj):
        return {
            'id': obj.id,
            'read_at': obj.read_at,
            'station': {
                'name': obj.station.name,
                'code': obj.station.code,
                'kind': obj.station.kind,
                'source': obj.station.source.identifier,
                'location': (
                    [obj.station.latlng.x, obj.station.latlng.y]
                    if obj.station.latlng else None
                ),
                'altitude': obj.station.altitude,
            },
            'values': obj.values,
        }

    def full_representation(self, obj):
        return {
            'id': obj.id,
            'read_at': obj.read_at,
            'values': obj.values,
            'station': {
                'code': obj.station.code,
                'name': obj.station.name,
                'kind': obj.station.kind,
                'location': (
                    [obj.station.latlng.x, obj.station.latlng.y]
                    if obj.station.latlng else None
                ),
                'altitude': obj.station.altitude,
                'interval': obj.station.interval,
                'sensors': [{
                    'name': sensor.name,
                    'identifier': sensor.identifier,
                    'measure_unit': sensor.measure_unit
                } for sensor in obj.station.sensors],
                'source': {
                    'name': obj.station.source.name,
                    'identifier': obj.station.source.identifier,
                    'url': obj.station.source.url,
                    'license': obj.station.source.license
                }
            }
        }

    @staticmethod
    def _parse_date(value):
        value = ciso8601.parse_datetime(value)

        if value is None:
            raise ApiError(u'Invalid end or start date/time', 400)

        return value

    def apply_filters(self, query, filters):
        start = filters.get('start')
        end = filters.get('end')
        station = filters.get('station')
        source = filters.get('source')
        kind = filters.get('kind')
        sensor = filters.get('sensor')
        bbox = filters.get('bbox')

        if start:
            start = DataResource._parse_date(start)
            query = query.filter(Data.read_at >= start)

        if end:
            end = DataResource._parse_date(end)
            query = query.filter(Data.read_at <= end)

        if station or kind or source or bbox:
            query = query.join(Station, Data.station_id == Station.id)

        if station:
            station = station.split(',')
            query = query.filter(Station.code.in_(station))

        if source:
            source = source.split(',')
            query = query.join(Source, Station.source_id == Source.id) \
                         .filter(Source.identifier.in_(source))

        if kind:
            kind = cast(kind.split(','), ARRAY(String))
            query = query.filter(Station.kind.overlap(kind))

        if sensor:
            sensor = sensor.split(',')
            query = query.join(SensorData,
                               SensorData.data_id == Data.id) \
                         .join(Sensor,
                               SensorData.sensor_id == Sensor.id) \
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

    def already_exists(self, data, current_obj=None):
        return False

    def populate_object(self, obj, data):
        obj.read_at = DataResource._parse_date(data['read_at'])

        station = Station.query.filter_by(code=data['station']).first()
        if station is None:
            raise ApiError('Station {} not found'.format(data['station']), 400)

        obj.station_id = station.id
        obj.sensor_data = []

        for sensor_value in data['values']:
            sensor_id = sensor_value['sensor']
            value = sensor_value['value']

            sensor = Sensor.query.join(StationSensor,
                                       StationSensor.sensor_id == Sensor.id) \
                                 .filter(Sensor.identifier == sensor_id,
                                         StationSensor.station_id == station.id) \
                                 .first()
            if sensor is None:
                raise ApiError('Sensor {} not found'.format(sensor_id), 400)

            if not sensor.validate_data(value):
                raise ApiError(
                    'Invaild value {} for sensor {}'.format(value, sensor_id),
                    400)

            sensor_data = SensorData(data=obj, sensor=sensor, value=value)
            obj.sensor_data.append(sensor_data)
