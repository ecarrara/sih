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
