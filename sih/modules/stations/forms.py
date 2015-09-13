# -*- coding: utf-8 -*-
"""
    sih.modules.stations.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_wtf import Form
from wtforms.fields import TextField
from wtforms.validators import DataRequired, URL


class SourceForm(Form):

    name = TextField(u'Nome', validators=[DataRequired()])
    identifier = TextField(u'Identificador', validators=[DataRequired()])
    url = TextField(u'URL', validators=[URL()])
    license = TextField(u'Licença')
