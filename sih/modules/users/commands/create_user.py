# -*- coding: utf-8 -*-
"""
    sih.modules.users.commands.create_user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""


from flask_script import Command, Option
from sih.extensions import db
from sih.modules.users.models import User


class CreateUserCommand(Command):

    option_list = (
        Option('--name', '-n', dest='name', required=True),
        Option('--username', '-u', dest='username', required=True),
        Option('--email', '-e', dest='email', required=True),
        Option('--password', '-p', dest='password', required=True),
        Option('--api-key', '-k', dest='api_key', required=False),
        Option('--roles', '-r', dest='roles', required=False, default='admin')
    )

    def run(self, name, username, email, password, api_key, roles):
        user = User(name=name, username=username, password=password,
                    email=email, roles=roles.split(','), status='active',
                    api_key=api_key)

        db.session.add(user)
        db.session.commit()
