# -*- coding: utf-8 -*-
"""
    sih.modules.geo.views.cities
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, request, flash, url_for, redirect
from flask_login import login_required
from sih.extensions import db
from sih.permissions import role_required
from sih.modules.geo import geo
from sih.modules.geo.models import City
from sih.modules.geo.forms import CityForm


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
    form = CityForm()

    if form.validate_on_submit():
        city = City()
        form.populate_obj(city)

        db.session.add(city)
        db.session.commit()

        flash(u'Cidade cadastrada com sucesso.', 'success')

        return redirect(url_for('geo.cities_view', city_id=city.id))

    return render_template('geo/cities/create.html', form=form)


@geo.route('/cities/<int:city_id>')
@login_required
@role_required(['admin'])
def cities_view(city_id):
    raise NotImplementedError()


@geo.route('/cities/<int:city_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def cities_edit(city_id):
    city = City.query.filter(City.id == city_id).first_or_404()

    form = CityForm(obj=city)
    if form.validate_on_submit():
        form.populate_obj(city)

        db.session.add(city)
        db.session.commit()

        flash(u'Cidade editada com sucesso.', 'success')

        return redirect(url_for('geo.cities_view', city_id=city.id))

    return render_template('geo/cities/edit.html', city=city, form=form)


@geo.route('/cities/<int:city_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def cities_delete(city_id):
    city = City.query.filter(City.id == city_id).first_or_404()

    db.session.delete(city)
    db.session.commit()

    flash(u'Cidade excluída com sucesso.', 'success')

    return redirect(url_for('geo.cities_list'))
