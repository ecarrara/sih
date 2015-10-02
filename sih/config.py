# -*- coding: utf-8 -*-
"""
    sih.config
    ~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from os import getenv


class BaseConfig(object):

    APPLICATION_NAME = 'SIH'
    SERVER_NAME = 'sih.eco.br'

    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', 'postgresql:///sih')
    ASSETS = 'sih/assets.yml'

    BABEL_DEFAULT_LOCALE = 'pt_BR'
    BABEL_DEFAULT_TIMEZONE = 'America/Sao_Paulo'

    SECRET_KEY = 'You fritter and waste the hours in an offhand way'


class DevelopmentConfig(BaseConfig):

    SERVER_NAME = 'sih.dev:5000'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', 'postgresql:///sih_dev')


class TestingConfig(BaseConfig):

    SERVER_NAME = 'localhost'       # workaround (see http://git.io/vnETx)
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', 'postgresql:///sih_test')

    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True


class ProductionConfig(BaseConfig):
    pass
