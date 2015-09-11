# -*- coding: utf-8 -*-
"""
    sih.extensions
    ~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Environment
from flask_login import LoginManager
from flask_babel import Babel


db = SQLAlchemy()
migrate = Migrate()
assets = Environment()
login_manager = LoginManager()
babel = Babel()
