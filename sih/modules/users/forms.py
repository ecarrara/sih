# -*- coding: utf-8 -*-
"""
    sih.modules.users.forms
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask_wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):

    username = TextField(u'Nome de usuário', validators=[DataRequired()])
    password = PasswordField(u'Senha', validators=[DataRequired()])
