#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from sih import create_app
from sih.config import DevelopmentConfig


app = create_app(DevelopmentConfig())
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
