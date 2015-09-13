# -*- coding: utf-8 -*-
"""
    sih.permissions
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(roles, http_code=403):
    """Verifica o papel do usuário.

    Executa a função decorada caso o usuário tenha ao menos um dos papéis,
    caso contrário aborta com o código http informado.

    :param roles: lista de papéis.
    :param http_code: código http de aborto (padrão 403).
    """

    def decorator(fn):
        @wraps(fn)
        def decorated_fn(*args, **kwargs):
            if not current_user.is_anonymous:
                for role in current_user.roles:
                    if role in roles:
                        return fn(*args, **kwargs)

            return abort(http_code)

        return decorated_fn

    return decorator
