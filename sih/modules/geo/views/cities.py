# -*- coding: utf-8 -*-
"""
    sih.modules.geo.views.cities
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, request
from flask_login import login_required
from sih.permissions import role_required
from sih.modules.geo import geo
from sih.modules.geo.models import City


@geo.route('/cities')
@login_required
@role_required(['admin'])
def cities_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    cities = City.query.order_by(City.name).paginate(page, per_page)

    return render_template('geo/cities/list.html', cities=cities)


@geo.route('/cities/create', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def cities_create():
    raise NotImplementedError()


@geo.route('/cities/<int:city_id>')
@login_required
@role_required(['admin'])
def cities_view(city_id):
    raise NotImplementedError()


@geo.route('/cities/<int:city_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def cities_edit(city_id):
    raise NotImplementedError()


@geo.route('/cities/<int:city_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def cities_delete(city_id):
    raise NotImplementedError()
