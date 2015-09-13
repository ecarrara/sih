# -*- coding: utf-8 -*-
"""
    sih.modules.stations.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

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
