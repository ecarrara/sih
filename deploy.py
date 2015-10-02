# -*- coding: utf-8 -*-

from sih import create_app
from sih.config import ProductionConfig

app = create_app(config=ProductionConfig())
