# -*- coding: utf-8 -*-
"""
    sih.modules.stations.views.sensors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, flash, url_for, redirect, request
from flask_login import login_required
from sih.extensions import db
from sih.permissions import role_required
from sih.modules.stations import stations
from sih.modules.stations.models import Sensor
from sih.modules.stations.forms import SensorForm


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
    form = SensorForm()
    if form.validate_on_submit():
        sensor = Sensor()
        form.populate_obj(sensor)

        db.session.add(sensor)
        db.session.commit()

        flash(u'Sensor cadastrado com sucesso.', 'success')

        return redirect(url_for('stations.sensors_list'))

    return render_template('stations/sensors/create.html', form=form)


@stations.route('/sensors/<int:sensor_id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def sensors_view(sensor_id):
    sensor = Sensor.query.filter(Sensor.id == sensor_id).first_or_404()

    user_input = request.form.get('input', None, type=int)
    validate_output = None
    validate_error = None
    process_output = None
    process_error = None

    if user_input:
        try:
            validate_output = sensor.validate_data(user_input)
        except Exception as e:
            validate_error = str(e)

        try:
            process_output = sensor.process_data(user_input)
        except Exception as e:
            process_error = str(e)

    return render_template('stations/sensors/view.html', sensor=sensor,
                           validate_output=validate_output,
                           validate_error=validate_error,
                           process_output=process_output,
                           process_error=process_error,
                           user_input=user_input)


@stations.route('/sensors/<int:sensor_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def sensors_edit(sensor_id):
    sensor = Sensor.query.filter(Sensor.id == sensor_id).first_or_404()
    form = SensorForm(obj=sensor)

    if form.validate_on_submit():
        form.populate_obj(sensor)

        db.session.add(sensor)
        db.session.commit()

        flash(u'Sensor editado com sucesso.', 'success')

        return redirect(url_for('stations.sensors_list'))

    return render_template('stations/sensors/edit.html',
                           form=form, sensor=sensor)


@stations.route('/sensors/<int:sensor_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def sensors_delete(sensor_id):
    sensor = Sensor.query.filter(Sensor.id == sensor_id).first_or_404()

    db.session.delete(sensor)
    db.session.commit()

    flash(u'Sensor excluído com sucesso.', 'success')

    return redirect(url_for('stations.sensors_list'))
