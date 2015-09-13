# -*- coding: utf-8 -*-
"""
    sih.json
    ~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""


from flask import json as _json
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry


class JSONEncoder(_json.JSONEncoder):

    def default(self, o):
        if isinstance(o, BaseGeometry):
            return mapping(o)

        return _json.JSONEncoder.default(self, o)
