# -*- coding: utf-8 -*-
"""
    sih
    ~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Flask, render_template
from sih.json import JSONEncoder
from sih.extensions import db, migrate, assets, login_manager, babel
from sih.modules import users, stations, geo, data, api
from sih.modules.users.models import User


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_envvar('SIH_CONFIG', silent=True)

    app.json_encoder = JSONEncoder

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

    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = u'Por favor faça login.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    babel.init_app(app)


def register_modules(app):
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(stations, url_prefix='/stations')
    app.register_blueprint(geo, url_prefix='/geo')
    app.register_blueprint(data, url_prefix='/data')
    app.register_blueprint(api, subdomain='api')
