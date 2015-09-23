# -*- coding: utf-8 -*-
"""
    sih.modules.api.views
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from sih.extensions import db


class ApiResource(object):

    model_class = None
    model_id = 'id'
    schema = None
    limit = 100

    def populate_object(self, data):
        raise NotImplementedError()

    def short_representation(self, obj):
        raise NotImplementedError()

    def full_representation(self, obj):
        raise NotImplementedError()

    def get_object(self, obj_id):
        id_field = getattr(self.model_class, self.model_id)
        return self.model_class.query \
                               .filter(id_field == obj_id) \
                               .first()

    def get_object_list(self, filters, offset, limit):
        query = self.model_class.query
        query = self.apply_filters(query, filters)
        return query.offset(offset).limit(limit).all()

    def total_count(self, filters):
        query = self.model_class.query
        query = self.apply_filters(query, filters)
        return query.count()

    def delete_object(self, obj):
        db.session.delete(obj)
        db.session.commit()

    def create_object(self, data):
        obj = self.model_class()

        self.populate_object(obj, data)

        db.session.add(obj)
        db.session.commit()

        return obj

    def edit_object(self, obj, data):
        self.populate_object(obj, data)

        db.session.add(obj)
        db.session.commit()

        return obj

    def apply_filters(self, query, filters):
        return query

    def validate_data(self, data):
        pass
