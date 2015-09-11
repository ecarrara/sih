# -*- coding: utf-8 -*-
"""
    sih.modules.users.models
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from sqlalchemy.event import listen
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import generate_password_hash, check_password_hash
from sih.extensions import db


class User(db.Model):

    __tablename__ = 'users'

    STATUS = {
        'active': u'Ativo',
        'inactive': u'Inativo'
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    roles = db.Column(ARRAY(db.String), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Enum(*STATUS.keys(), name='user_status'),
                       nullable=False, default='inactive')
    api_key = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# generate password hash
listen(User.password, 'set', lambda t, v, o, i: generate_password_hash(v),
       retval=True)
