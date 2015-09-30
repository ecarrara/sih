# -*- coding: utf-8 -*-
"""
    sih.modules.geo
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Blueprint


geo = Blueprint('geo', __name__, template_folder='templates')


from sih.modules.geo.views.cities import *          # noqa
from sih.modules.geo.views.basins import *          # noqa
