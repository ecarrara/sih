# -*- coding: utf-8 -*-
"""
    sih.modules.stations.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from geoalchemy2.types import Geography
from geoalchemy2.shape import to_shape
from sqlalchemy.dialects.postgresql import ARRAY
from sih.extensions import db


class Source(db.Model):

    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(255), nullable=True)
    license = db.Column(db.String(64), nullable=True)


class Sensor(db.Model):

    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    identifier = db.Column(db.String(32), nullable=False, unique=True)
    measure_unit = db.Column(db.String(32), nullable=False)
    validate_code = db.Column(db.Text, nullable=True)
    process_code = db.Column(db.Text, nullable=True)

    def _run_code(self, code, scope=None):
        code = compile(code, filename='<string>', mode='exec')

        ctx = {}
        if scope is not None:
            ctx.update(scope)

        eval(code, {'__builtins__': {}}, ctx)
        return ctx

    def validate_data(self, value):
        if not self.validate_code:
            return True

        ctx = self._run_code(self.validate_code, {'value': value})
        return bool(ctx.get('result'))

    def process_data(self, value, station=None, data=None):
        if not self.process_code:
            return value

        ctx = self._run_code(self.process_code, {
            'value': value,
            'station': station,
            'data': data
        })

        result = ctx.get('result')
        return int(result) if result is not None else None


class StationSensor(db.Model):

    __tablename__ = 'stations_sensors'
    __table_args__ = (
        db.UniqueConstraint('station_id', 'sensor_id',
                            name='uq_stations_sensors_station_sensor'),
    )

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'),
                           nullable=False, index=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'),
                          nullable=False, index=True)


class Station(db.Model):

    __tablename__ = 'stations'

    KINDS = {
        'pluviometric': u'Pluviométrica',
        'barrage': u'Barragem',
        'fluviometric': u'Fluviométrica',
        'quality': u'Qualidade',
        'meterologic': u'Meteorológica'
    }

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False, unique=True, index=True)
    name = db.Column(db.String(256), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    installed_at = db.Column(db.DateTime, nullable=True)
    kind = db.Column(ARRAY(db.String(32)), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    source_id = db.Column(db.ForeignKey('sources.id', ondelete='SET NULL'),
                          nullable=False)
    location = db.Column(Geography('POINT'), nullable=True, index=True)
    altitude = db.Column(db.Integer(), nullable=True)
    interval = db.Column(db.Integer, nullable=False, default=15)

    source = db.relationship('Source')
    sensors = db.relationship('Sensor', lazy='dynamic',
                              backref=db.backref('stations', lazy='dynamic'),
                              secondary=lambda: StationSensor.__table__)

    @property
    def latlng(self):
        if self.location is not None:
            return to_shape(self.location)
