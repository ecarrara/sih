# -*- coding: utf-8 -*-
"""
    sih.modules.geo.views.basins
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, flash, url_for, redirect
from flask_login import login_required
from sih.extensions import db
from sih.permissions import role_required
from sih.modules.geo import geo
from sih.modules.geo.models import Basin
from sih.modules.geo.forms import BasinForm


@geo.route('/basins')
@login_required
@role_required(['admin'])
def basins_list():
    basins = Basin.query.all()
    return render_template('geo/basins/list.html', basins=basins)


@geo.route('/basins/create', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def basins_create():
    form = BasinForm()

    if form.validate_on_submit():
        basin = Basin()
        form.populate_obj(basin)

        db.session.add(basin)
        db.session.commit()

        flash(u'Bacia cadastrada com sucesso.', 'success')

        return redirect(url_for('geo.basins_view', basin_id=basin.ottocode))

    return render_template('geo/basins/create.html', form=form)


@geo.route('/basins/<basin_id>')
@login_required
@role_required(['admin'])
def basins_view(basin_id):
    basin = Basin.query.filter(Basin.ottocode == basin_id).first_or_404()
    return render_template('geo/basins/view.html', basin=basin)


@geo.route('/basins/<basin_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def basins_edit(basin_id):
    raise NotImplementedError()


@geo.route('/basins/<basin_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def basins_delete(basin_id):
    raise NotImplementedError()
