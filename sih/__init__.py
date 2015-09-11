# -*- coding: utf-8 -*-
"""
    sih
    ~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Flask, render_template
from sih.extensions import db, migrate, assets
from sih.modules import users


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_envvar('SIH_CONFIG', silent=True)

    configure_extensions(app)
    register_modules(app)

    @app.route('/')
    def home():
        return 'The lunatic is in my head'

    @app.route('/__ui')
    def ui():
        return render_template('ui.html')

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

    assets.init_app(app)
    assets.from_yaml(app.config['ASSETS'])


def register_modules(app):
    app.register_blueprint(users, url_prefix='/users')
