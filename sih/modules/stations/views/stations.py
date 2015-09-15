# -*- coding: utf-8 -*-
"""
    sih.modules.stations.views.stations
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, request, flash, url_for, redirect
from flask_login import login_required
from sih.extensions import db
from sih.permissions import role_required
from sih.modules.stations import stations
from sih.modules.stations.models import Station
from sih.modules.stations.forms import StationForm


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
    form = StationForm()

    if form.validate_on_submit():
        station = Station()
        form.populate_obj(station)

        db.session.add(station)
        db.session.commit()

        flash(u'Estação cadastrada com sucesso.', 'success')

        return redirect(url_for('stations.stations_view',
                                station_id=station.id))

    return render_template('stations/stations/create.html', form=form)


@stations.route('/stations/<int:station_id>')
@login_required
@role_required(['admin'])
def stations_view(station_id):
    raise NotImplementedError()


@stations.route('/stations/<int:station_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def stations_edit(station_id):
    station = Station.query.filter(Station.id == station_id).first_or_404()
    form = StationForm(obj=station)

    if form.validate_on_submit():
        form.populate_obj(station)

        db.session.add(station)
        db.session.commit()

        flash(u'Estação alterada com sucesso.', 'success')

        return redirect(url_for('stations.stations_view',
                                station_id=station.id))

    return render_template('stations/stations/edit.html',
                           station=station, form=form)


@stations.route('/stations/<int:station_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def stations_delete(station_id):
    raise NotImplementedError()
