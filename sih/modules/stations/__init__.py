# -*- coding: utf-8 -*-
"""
    sih.modules.stations
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Blueprint


stations = Blueprint('stations', __name__, template_folder='templates')


from sih.modules.stations.views.sources import *        # noqa
