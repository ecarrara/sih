# -*- coding: utf-8 -*-
"""
    sih.config
    ~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""


class BaseConfig(object):
    pass


class DevelopmentConfig(BaseConfig):

    DEBUG = True


class TestingConfig(BaseConfig):

    TESTING = True
