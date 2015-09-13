# -*- coding: utf-8 -*-
"""
    sih.modules.stations.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_wtf import Form
from wtforms.fields import TextField, TextAreaField
from wtforms.validators import DataRequired, URL, ValidationError


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
