# -*- coding: utf-8 -*-
"""
    sih.forms.validators
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from wtforms.validators import ValidationError


class GreaterThan(object):

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(
                field.gettext(u"Invalid field name '%s'.") % self.fieldname
            )

        if field.data > other.data:
            return

        message = self.message
        if message is None:
            message = field.gettext(
                u'Field must be greater than %(other_name)s.'
            )

        raise ValidationError(message % {
            'other_label': other.label.text,
            'other_name': self.fieldname
        })
