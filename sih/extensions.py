# -*- coding: utf-8 -*-
"""
    sih.extensions
    ~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
