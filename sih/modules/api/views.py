# -*- coding: utf-8 -*-
"""
    sih.modules.api.view
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""


from flask import request, jsonify
from flask.views import View
from sih.modules.api.exceptions import ApiError


class ApiView(View):

    def __init__(self, resource):
        self.resource = resource

    @classmethod
    def register(cls, app, name, url_prefix, resource):
        view = cls.as_view(name, resource=resource)

        app.add_url_rule(url_prefix,
                         view_func=view,
                         methods=['GET', 'POST'])

        app.add_url_rule('{0}/<obj_id>'.format(url_prefix),
                         view_func=view,
                         methods=['GET', 'PUT', 'DELETE'],)

    def dispatch_request(self, obj_id=None):
        try:
            if obj_id is None:
                if request.method == 'POST':
                    return self.create()
                return self.list()

            if request.method == 'GET':
                return self.view(obj_id)
            elif request.method == 'PUT':
                return self.edit(obj_id)
            elif request.method == 'DELETE':
                return self.delete(obj_id)

        except ApiError as e:
            return jsonify({
                'message': str(e)
            }), e.code

    def request_data(self):
        data = request.get_json(silent=True)
        self.resource.validate_data(data)
        return data

    def list(self):
        args = request.args.copy()

        offset = int(args.pop('offset', 0))
        limit = int(args.pop('limit', self.resource.limit))

        if limit > self.resource.limit:
            limit = self.resource.limit

        objects = self.resource.get_object_list(filters=args,
                                                offset=offset, limit=limit)

        return jsonify({
            'data': [
                self.resource.short_representation(obj) for obj in objects
            ],
            'summary': {
                'total': self.resource.total_count(filters=args),
                'result_size': len(objects),
                'offset': offset
            }
        })

    def view(self, obj_id):
        obj = self.resource.get_object(obj_id)

        if obj is None:
            raise ApiError('Not found', 404)

        return jsonify(self.resource.full_representation(obj))

    def create(self):
        data = self.request_data()
        obj = self.resource.create_object(data)

        return jsonify(self.resource.full_representation(obj)), 201

    def edit(self, obj_id):
        obj = self.resource.get_object(obj_id)

        data = self.request_data()
        obj = self.resource.edit_object(obj, data)

        return jsonify(self.resource.full_representation(obj))

    def delete(self, obj_id):
        obj = self.resource.get_object(obj_id)

        if obj is None:
            raise ApiError(u'Not found', 404)

        self.resource.delete_object(obj)

        return '', 204
