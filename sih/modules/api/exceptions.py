# -*- coding: utf-8 -*-
"""
    sih.modules.api.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""


class ApiError(Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message
