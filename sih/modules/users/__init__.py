# -*- coding: utf-8 -*-
"""
    sih.modules.users
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Blueprint


users = Blueprint('users', __name__, template_folder='templates')
