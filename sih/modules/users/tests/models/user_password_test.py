# -*- coding: utf-8 -*-
"""
    sih.modules.users.tests.models.user_password_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.tests import TestCase
from sih.modules.users.models import User


class UserPasswordTestCase(TestCase):

    def setUp(self):
        super(UserPasswordTestCase, self).setUp()
        self.user = User(name='Test',
                         email='test@example.com',
                         password='secret')

    def test_hash_password(self):
        self.assertNotEquals(self.user.password, 'secret')

    def test_check_password(self):
        self.assertTrue(self.user.check_password('secret'))
