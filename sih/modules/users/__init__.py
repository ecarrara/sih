# -*- coding: utf-8 -*-
"""
    sih.modules.users
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import Blueprint, redirect, render_template, flash
from flask_login import login_user
from sih.modules.users.models import User
from sih.modules.users.forms import LoginForm


users = Blueprint('users', __name__, template_folder='templates')


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')

        flash(u'Usuário e/ou senha inválidos.', 'warning')

    return render_template('users/login.html', form=form)
