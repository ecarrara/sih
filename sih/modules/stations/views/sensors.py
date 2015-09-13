# -*- coding: utf-8 -*-
"""
    sih.modules.stations.views.sensors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template
from flask_login import login_required
from sih.permissions import role_required
from sih.modules.stations import stations
from sih.modules.stations.models import Sensor


@stations.route('/sensors')
@login_required
@role_required(['admin'])
def sensors_list():
    sensors = Sensor.query.order_by(Sensor.name).all()
    return render_template('stations/sensors/list.html', sensors=sensors)


@stations.route('/sensors/create', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def sensors_create():
    raise NotImplementedError()


@stations.route('/sensors/<int:sensor_id>')
@login_required
@role_required(['admin'])
def sensors_view(sensor_id):
    raise NotImplementedError()


@stations.route('/sensors/<int:sensor_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def sensors_edit(sensor_id):
    raise NotImplementedError()


@stations.route('/sensors/<int:sensor_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def sensors_delete(sensor_id):
    raise NotImplementedError()
