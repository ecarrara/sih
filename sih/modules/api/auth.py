# -*- coding: utf-8 -*-
"""
    sih.modules.api.auth
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from base64 import b64encode


def basic_auth(username, password):
    return u'Basic {}'.format(b64encode('{}:{}'.format(username, password)))
