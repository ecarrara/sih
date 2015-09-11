# -*- coding: utf-8 -*-
"""
    sih.modules.users.tests.views.login_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import url_for
from flask_login import current_user
from sih.tests import TestCase
from sih.extensions import db
from sih.modules.users.models import User


class LoginTestCase(TestCase):

    def test_wrong_login(self):
        url = url_for('users.login')

        with self.client:
            response = self.client.post(url, data={
                'username': 'wrong',
                'password': 'test123'
            })

            self.assert200(response)
            self.assertTrue(current_user.is_anonymous)

    def test_valid_login(self):

        user = User(name='Test 1', email='test@example.com',
                    username='test1', password='test123', status='active')
        db.session.add(user)

        with self.client:
            response = self.client.post(url_for('users.login'), data={
                'username': 'test1',
                'password': 'test123'
            })

            self.assertRedirects(response, '/')
            self.assertTrue(current_user.is_active)
            self.assertTrue(current_user.is_authenticated)
            self.assertFalse(current_user.is_anonymous)
