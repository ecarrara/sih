# -*- coding: utf-8 -*-
"""
    sih
    ~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Flask
from sih.extensions import db, migrate


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_envvar('SIH_CONFIG', silent=True)

    configure_extensions(app)

    @app.route('/')
    def home():
        return 'The lunatic is in my head'

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
