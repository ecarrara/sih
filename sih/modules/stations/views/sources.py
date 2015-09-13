# -*- coding: utf-8 -*-
"""
    sih.modules.stations.views.sources
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template
from flask_login import login_required
from sih.permissions import role_required
from sih.modules.stations import stations
from sih.modules.stations.models import Source


@stations.route('/sources')
@login_required
@role_required(['admin'])
def sources_list():
    sources = Source.query.order_by(Source.name).all()
    return render_template('stations/sources/list.html', sources=sources)


@stations.route('/sources/create', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def sources_create():
    raise NotImplementedError()


@stations.route('/sources/<int:source_id>')
@login_required
@role_required(['admin'])
def sources_view(source_id):
    raise NotImplementedError()


@stations.route('/sources/<int:source_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def sources_edit(source_id):
    raise NotImplementedError()


@stations.route('/sources/<int:source_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def sources_delete(source_id):
    raise NotImplementedError()
