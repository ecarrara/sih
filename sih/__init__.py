# -*- coding: utf-8 -*-
"""
    sih
    ~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Flask


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_envvar('SIH_CONFIG', silent=True)

    @app.route('/')
    def home():
        return 'The lunatic is in my head'

    return app
