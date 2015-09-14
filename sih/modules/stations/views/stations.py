# -*- coding: utf-8 -*-
"""
    sih.modules.stations.views.stations
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, request
from flask_login import login_required
from sih.permissions import role_required
from sih.modules.stations import stations
from sih.modules.stations.models import Station


@stations.route('/stations')
@login_required
@role_required(['admin'])
def stations_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    kind = request.args.get('kind')

    query = Station.query

    if kind:
        query = query.filter(Station.kind.any(kind))

    stations = query.order_by(Station.name).paginate(page, per_page)

    return render_template('stations/stations/list.html',
                           stations=stations,
                           kinds=Station.KINDS.items())


@stations.route('/stations/create', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def stations_create():
    raise NotImplementedError()


@stations.route('/stations/<int:station_id>')
@login_required
@role_required(['admin'])
def stations_view(station_id):
    raise NotImplementedError()


@stations.route('/stations/<int:station_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def stations_edit(station_id):
    raise NotImplementedError()


@stations.route('/stations/<int:station_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def stations_delete(station_id):
    raise NotImplementedError()
