# -*- coding: utf-8 -*-
"""
    sih.forms.fields
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from six import text_type
from wtforms.fields import TextField


class ListField(TextField):

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = map(text_type.strip, valuelist[0].split(u','))

    def _value(self):
        return u', '.join(self.data) if self.data else ''
