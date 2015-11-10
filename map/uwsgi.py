# -*- coding: utf-8 -*-

from logging.config import fileConfig
import os.path

fileConfig(r'conf/log.ini', {
    'here': os.path.dirname(__file__)
})

from mapproxy.wsgiapp import make_wsgi_app
application = make_wsgi_app(r'conf/mapproxy.yaml')
