# -*- coding: utf-8 -*-
"""
    sih.modules.geo.forms
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_wtf import Form
from wtforms.fields import TextField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms_geo.fields import PolygonField
from sih.modules.geo.models import STATES, City


class CityForm(Form):

    id = IntegerField(u'Código', validators=[DataRequired()])
    name = TextField(u'Nome', validators=[DataRequired()])
    state = SelectField(u'Estado', choices=STATES)
    boundary = PolygonField(u'Limites do Município')

    def __init__(self, obj=None, **kwargs):
        super(CityForm, self).__init__(obj=obj, **kwargs)
        self.obj = obj

    def validate_id(self, field):
        if self.obj and field.data == self.obj.id:
            return

        city = City.query.filter(City.id == field.data).first()
        if city:
            raise ValidationError(u'Código já registrado.')
