# -*- coding: utf-8 -*-
"""
    sih.modules.geo.models
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from geoalchemy2.types import Geography
from geoalchemy2.shape import to_shape
from sih.extensions import db


STATES = (
    ('AC', u'Acre'),
    ('AL', u'Alagoas'),
    ('AP', u'Amapá'),
    ('AM', u'Amazonas'),
    ('BA', u'Bahia'),
    ('CE', u'Ceará'),
    ('DF', u'Distrito Federal'),
    ('ES', u'Espirito Santo'),
    ('GO', u'Goiás'),
    ('MA', u'Maranhão'),
    ('MT', u'Mato Grosso'),
    ('MS', u'Mato Grosso do Sul'),
    ('MG', u'Minas Gerais'),
    ('PA', u'Pará'),
    ('PB', u'Paraíba'),
    ('PR', u'Paraná'),
    ('PE', u'Pernambuco'),
    ('PI', u'Piauí'),
    ('RJ', u'Rio de Janeiro'),
    ('RN', u'Rio Grande do Norte'),
    ('RS', u'Rio Grande do Sul'),
    ('RO', u'Rondônia'),
    ('SC', u'Santa Catarina'),
    ('SP', u'São Paulo'),
    ('SE', u'Sergipe'),
    ('TO', u'Tocantins')
)


class City(db.Model):

    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    boundary = db.Column(Geography('POLYGON'), index=True)
    center = db.Column(Geography('POINT'), index=True)

    def __str__(self):
        return u'{}/{}'.format(self.name, self.state)

    @property
    def boundary_shape(self):
        if self.boundary is not None:
            return to_shape(self.boundary)

    @property
    def center_shape(self):
        if self.center is not None:
            return to_shape(self.center)


class Basin(db.Model):

    __tablename__ = 'basins'

    ottocode = db.Column(db.String(12), primary_key=True)
    boundary = db.Column(Geography('POLYGON'), index=True)

    @property
    def boundary_shape(self):
        if self.boundary is not None:
            return to_shape(self.boundary)
