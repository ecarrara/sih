# -*- coding: utf-8 -*-
"""
    sih.modules.users.tests.commands.create_user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.tests import TestCase
from sih.modules.users.commands import CreateUserCommand
from sih.modules.users.models import User


class CreateUserCommandTestCase(TestCase):

    def test_create_user(self):
        """Deve ser possível criar um novo usuário ativo no sistema
        através do comando `create-user`.
        """

        command = CreateUserCommand()
        command.run('Test', 'test', 'test@example.com',
                    'test123', 'secretkey', 'admin,api')

        user = User.query.filter_by(name='Test', username='test',
                                    email='test@example.com').first()

        self.assertIsNotNone(user)
        self.assertEquals(user.name, 'Test')
        self.assertEquals(user.username, 'test')
        self.assertEquals(user.email, 'test@example.com')
        self.assertEquals(user.roles, ['admin', 'api'])
        self.assertEquals(user.api_key, 'secretkey')
