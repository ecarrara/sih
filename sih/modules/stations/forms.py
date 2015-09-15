# -*- coding: utf-8 -*-
"""
    sih.modules.stations.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_wtf import Form
from wtforms.fields import TextField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, URL, ValidationError
from wtforms.ext.sqlalchemy.fields import (QuerySelectField,
                                           QuerySelectMultipleField)
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms_geo.fields import PointField
from sih.forms.fields import ListField
from sih.modules.stations.models import Sensor, Source, Station


class SourceForm(Form):

    name = TextField(u'Nome', validators=[DataRequired()])
    identifier = TextField(u'Identificador', validators=[DataRequired()])
    url = TextField(u'URL', validators=[URL()])
    license = TextField(u'Licença')


class SensorForm(Form):

    name = TextField(u'Nome', validators=[DataRequired()])
    identifier = TextField(u'Identificador', validators=[DataRequired()])
    measure_unit = TextField(u'Unidade de Medida', validators=[DataRequired()])
    validate_code = TextAreaField(u'Código de Validação')
    process_code = TextAreaField(u'Código de Processamento')

    def _validate_code(self, field):
        invalid_tokens = ['_', 'eval']
        for token in invalid_tokens:
            if token in field.data:
                msg = u'Sequências não permitidas ({0}) encontradas.'
                raise ValidationError(msg.format(', '.join(invalid_tokens)))

        try:
            compile(field.data, filename='<string>', mode='exec')
        except SyntaxError as e:
            msg = u'Erro de sintaxe (linha {0}, coluna {1}): {2}'
            raise ValidationError(msg.format(e.lineno, e.offset, e.text))

    def validate_validate_code(self, field):
        self._validate_code(field)

    def validate_process_code(self, field):
        self._validate_code(field)


class StationForm(Form):
    name = TextField(u'Nome', validators=[DataRequired()])
    code = TextField(u'Código', validators=[DataRequired()])
    kind = ListField(u'Tipo', validators=[DataRequired()])
    installed_at = DateTimeField(u'Data da Instalação',
                                 parse_kwargs=dict(dayfirst=True),
                                 validators=[DataRequired()])
    description = TextAreaField(u'Descrição')
    source = QuerySelectField(u'Fonte', query_factory=lambda: Source.query,
                              get_label='name', allow_blank=False)
    altitude = IntegerField(u'Altitude')
    location = PointField(u'Localização')
    sensors = QuerySelectMultipleField('Sensores',
                                       query_factory=lambda: Sensor.query,
                                       get_label='name')
    interval = IntegerField(u'Intervalo dos Dados', default=15,
                            validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(StationForm, self).__init__(*args, **kwargs)
        self.obj = kwargs.get('obj')

    def validate_code(self, field):
        if self.obj and field.data == self.obj.code:
            return

        if Station.query.filter(Station.code == field.data).first():
            raise ValidationError(u'Código já cadastrado.')

    def validate_kind(self, field):
        if not field.data:
            return

        kinds = Station.KINDS.keys()

        for item in field.data:
            if item not in kinds:
                raise ValidationError(u'Tipo {} inválido.'.format(item))
