# -*- coding: utf-8 -*-
"""
    sih.modules.data.models
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Erle Carrara.
"""

from datetime import datetime
from sqlalchemy import event
from sih.extensions import db


class Data(db.Model):

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    read_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    sent_at = db.Column(db.DateTime(timezone=True), nullable=True)
    received_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            default=datetime.utcnow)
    station_id = db.Column(db.Integer,
                           db.ForeignKey('stations.id',
                                         ondelete='CASCADE',
                                         onupdate='CASCADE'),
                           nullable=False, index=True)

    sensor_data = db.relationship('SensorData', lazy='joined',
                                  cascade='all, delete-orphan')
    station = db.relationship('Station', lazy='joined',
                              backref=db.backref('data', lazy='dynamic',
                                                 order_by=read_at.desc()))

    __table_args__ = (
        db.UniqueConstraint('station_id', 'read_at',
                            name='uq_data_station_id_read_at'),
    )

    @property
    def values(self):
        return {
            sensor_data.sensor.identifier: sensor_data.value
            for sensor_data in self.sensor_data
        }


class SensorData(db.Model):

    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True)
    data_id = db.Column(db.Integer,
                        db.ForeignKey('data.id',
                                      ondelete='CASCADE',
                                      onupdate='CASCADE'),
                        nullable=False,
                        index=True)
    sensor_id = db.Column(db.Integer,
                          db.ForeignKey('sensors.id',
                                        ondelete='CASCADE',
                                        onupdate='CASCADE'),
                          nullable=False,
                          index=True)
    value = db.Column(db.Integer, index=True)

    data = db.relationship('Data', uselist=False)
    sensor = db.relationship('Sensor', uselist=False)

    __table_args__ = (
        db.UniqueConstraint('data_id', 'sensor_id',
                            name='uq_sensor_data_data_id_sensor_id'),
    )

    @staticmethod
    def before_insert(mapper, connection, target):
        if not target.data:
            return

        target.value = target.sensor.process_data(target.value,
                                                  station=target.data.station,
                                                  data=target.data)


event.listen(SensorData, 'before_insert', SensorData.before_insert)
