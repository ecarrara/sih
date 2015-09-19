# -*- coding: utf-8 -*-
"""
    sih.modules.data.form
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from pytz import timezone, utc
from flask_wtf import Form
from wtforms.fields import TextField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sih.modules.stations.models import Station, Sensor
from sih.modules.data.models import SensorData


class SensorDataForm(Form):
    sensor = QuerySelectField(u'Sensor', validators=[DataRequired()],
                              query_factory=lambda: Sensor.query,
                              allow_blank=False,
                              get_label='name')
    value = TextField(u'Valor')

    def validate_value(self, field):
        if not field.data:
            return

        try:
            field.data = int(field.data)
        except ValueError:
            raise ValidationError(u'O valor informado não é um número')

        if not self.sensor.data.validate_data(field.data):
            raise ValidationError(u'Valor inválido para o '
                                  u'sensor {0}'.format(self.sensor.data.name))


class DataForm(Form):

    _local_tz = timezone('America/Sao_Paulo')
    _default_datetime = datetime(1990, 1, 1)
    _datetime_format = '%Y-%m-%dT%H:%M:%S'

    station = QuerySelectField(u'Estação', validators=[DataRequired()],
                               query_factory=lambda: Station.query,
                               allow_blank=False,
                               get_label='name')
    read_at = DateTimeField(u'Data/Hora da Letura',
                            display_format=_datetime_format,
                            parse_kwargs=dict(default=_default_datetime),
                            validators=[DataRequired()])
    sensor_data = FieldList(FormField(SensorDataForm))

    def __init__(self, station, formdata=None, **kwargs):
        super(DataForm, self).__init__(**kwargs)

        if len(self.sensor_data) > 0:
            return

        for sensor in station.sensors:
            self.sensor_data.append_entry({
                'sensor': sensor,
                'value': None
            })

    def populate_obj(self, obj):
        obj.sent_at = datetime.utcnow().replace(tzinfo=utc)
        obj.read_at = self.read_at.data
        obj.station = self.station.data

        SensorData.query.filter(SensorData.data == obj).delete()

        for sensor_form in self.sensor_data:
            if sensor_form.value.data:
                new_sensor = SensorData(data=obj,
                                        sensor=sensor_form.sensor.data,
                                        value=sensor_form.value.data)
                obj.sensor_data.append(new_sensor)

    def validate_read_at(self, field):
        field.data = self._local_tz.localize(field.data)
        if field.data > datetime.now().replace(tzinfo=self._local_tz):
            raise ValidationError(u'Não é permitido o cadastro de '
                                  u'datas no futuro')
