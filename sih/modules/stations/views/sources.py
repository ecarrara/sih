# -*- coding: utf-8 -*-
"""
    sih.modules.stations.views.sources
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from sih.extensions import db
from sih.permissions import role_required
from sih.modules.stations import stations
from sih.modules.stations.models import Source
from sih.modules.stations.forms import SourceForm


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
    form = SourceForm()
    if form.validate_on_submit():
        source = Source()
        form.populate_obj(source)

        db.session.add(source)
        db.session.commit()

        flash(u'Fonte de dados cadastrada com sucesso.', 'success')

        return redirect(url_for('stations.sources_list'))

    return render_template('stations/sources/create.html', form=form)


@stations.route('/sources/<int:source_id>')
@login_required
@role_required(['admin'])
def sources_view(source_id):
    source = Source.query.filter(Source.id == source_id).first_or_404()
    return render_template('stations/sources/view.html', source=source)


@stations.route('/sources/<int:source_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def sources_edit(source_id):
    source = Source.query.filter(Source.id == source_id).first_or_404()
    form = SourceForm(obj=source)

    if form.validate_on_submit():
        form.populate_obj(source)

        db.session.add(source)
        db.session.commit()

        flash(u'Fonte de dados editada com sucesso.', 'success')

        return redirect(url_for('stations.sources_list'))

    return render_template('stations/sources/edit.html',
                           form=form, source=source)


@stations.route('/sources/<int:source_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def sources_delete(source_id):
    source = Source.query.filter(Source.id == source_id).first_or_404()

    db.session.delete(source)
    db.session.commit()

    flash(u'Fonte de dados excluída com sucesso.', 'success')

    return redirect(url_for('stations.sources_list'))
