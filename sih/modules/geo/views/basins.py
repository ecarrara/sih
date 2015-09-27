# -*- coding: utf-8 -*-
"""
    sih.modules.geo.views.basins
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template
from flask_login import login_required
from sih.permissions import role_required
from sih.modules.geo import geo
from sih.modules.geo.models import Basin


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
    raise NotImplementedError()


@geo.route('/basins/<basin_id>')
@login_required
@role_required(['admin'])
def basins_view(basin_id):
    raise NotImplementedError()


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