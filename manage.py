#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import MigrateCommand
from flask_assets import ManageAssets
from sih import create_app
from sih.config import DevelopmentConfig
from sih.modules.users.commands import CreateUserCommand


app = create_app(DevelopmentConfig())
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets())
manager.add_command('create_user', CreateUserCommand())

if __name__ == '__main__':
    manager.run()
