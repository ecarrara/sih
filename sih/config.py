# -*- coding: utf-8 -*-
"""
    sih.config
    ~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from os import getenv


class BaseConfig(object):

    APPLICATION_NAME = 'SIH'

    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', 'postgresql:///sih')
    ASSETS = 'sih/assets.yml'


class DevelopmentConfig(BaseConfig):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', 'postgresql:///sih_dev')


class TestingConfig(BaseConfig):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', 'postgresql:///sih_test')
