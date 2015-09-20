# -*- coding: utf-8 -*-
"""
    sih.modules.data.views.stations
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from sih.forms import DateTimeFilterForm
from sih.extensions import db
from sih.permissions import role_required
from sih.modules.data import data
from sih.modules.data.models import Data
from sih.modules.data.forms import DataForm
from sih.modules.stations.models import Station


@data.route('/stations/<int:station_id>')
@login_required
@role_required(['admin'])
def stations_view(station_id):
    station = Station.query.filter(Station.id == station_id).first_or_404()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 96, type=int)

    query = station.data

    filter_form = DateTimeFilterForm(request.args)
    if filter_form.validate():
        query = query.filter(
            Data.read_at.between(filter_form.start.data,
                                 filter_form.end.data)
        )

    data = query.paginate(page, per_page)

    return render_template('data/stations/view.html',
                           station=station, data=data,
                           filter_form=filter_form)


@data.route('/stations/<int:station_id>/create', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def stations_create(station_id):
    station = Station.query.filter(Station.id == station_id).first_or_404()

    form = DataForm(station=station)
    if form.validate_on_submit():
        data = Data()
        form.populate_obj(data)

        db.session.add(data)
        db.session.commit()

        flash(u'Dado cadastrado com sucesso.', 'success')

        return redirect(url_for('data.stations_view', station_id=station.id))

    return render_template('data/stations/create.html',
                           form=form, station=station)


@data.route('/stations/<int:station_id>/<int:data_id>/edit',
            methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def stations_edit(station_id, data_id):
    data = Data.query \
               .filter(Data.id == data_id,
                       Data.station_id == station_id) \
               .first_or_404()

    form = DataForm(station=data.station, obj=data)
    if form.validate_on_submit():
        form.populate_obj(data)

        db.session.add(data)
        db.session.commit()

        url = url_for('data.stations_view', station_id=data.station.id)
        return redirect(url)

    return render_template('data/stations/edit.html',
                           form=form, data=data, station=data.station)


@data.route('/stations/<int:station_id>/<int:data_id>/delete',
            methods=['POST'])
@login_required
@role_required(['admin'])
def stations_delete(station_id, data_id):
    data = Data.query \
               .filter(Data.id == data_id,
                       Data.station_id == station_id) \
               .first_or_404()

    db.session.delete(data)
    db.session.commit()

    flash(u'Dado excluído com sucesso.', 'success')

    return redirect(url_for('data.stations_view', station_id=station_id))
