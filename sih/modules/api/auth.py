# -*- coding: utf-8 -*-
"""
    sih.modules.api.auth
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from base64 import b64encode


def basic_auth(username, password):
    auth = '{}:{}'.format(username, password)
    return 'Basic {}'.format(b64encode(auth.encode('utf-8')).decode('utf-8'))
