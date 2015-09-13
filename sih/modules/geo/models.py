# -*- coding: utf-8 -*-
"""
    sih.modules.geo.models
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from geoalchemy2.types import Geography
from sih.extensions import db


class City(db.Model):

    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    boundary = db.Column(Geography('POLYGON'), index=True)
    center = db.Column(Geography('POINT'), index=True)
