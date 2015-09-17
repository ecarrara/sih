# -*- coding: utf-8 -*-
"""
    sih.forms
    ~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_wtf import Form
from wtforms.ext.dateutil.fields import DateTimeField
from sih.forms.validators import GreaterThan


class DateTimeFilterForm(Form):

    start = DateTimeField(u'Início',
                          parse_kwargs=dict(dayfirst=True))
    end = DateTimeField(u'Fim',
                        parse_kwargs=dict(dayfirst=True),
                        validators=[
                            GreaterThan('start',
                                        u'Data final deve ser posterior '
                                        u'à data inicial.')
                        ])

    def __init__(self, *args, **kwargs):
        super(DateTimeFilterForm, self).__init__(csrf_enabled=False,
                                                 *args, **kwargs)

    def validate(self):
        if self.start.data and self.end.data:
            return super(DateTimeFilterForm, self).validate()
