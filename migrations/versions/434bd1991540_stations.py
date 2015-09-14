# -*- coding: utf-8 -*-
"""stations

Revision ID: 434bd1991540
Revises: 714115f5625
Create Date: 2015-09-13 20:55:42.660698

"""

# revision identifiers, used by Alembic.
revision = '434bd1991540'
down_revision = '714115f5625'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from geoalchemy2.types import Geography


def upgrade():
    op.create_table(
        'stations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('installed_at', sa.DateTime(), nullable=True),
        sa.Column('kind', ARRAY(sa.String(length=32)), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('location', Geography('POINT'), nullable=True),
        sa.Column('altitude', sa.Integer(), nullable=True),
        sa.Column('interval', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'],
                                ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stations_code'), 'stations',
                    ['code'], unique=True)
    op.create_index(op.f('ix_stations_kind'), 'stations',
                    ['kind'], unique=False)
    op.create_index(op.f('ix_stations_location'), 'stations',
                    ['location'], unique=False)
    op.create_index(op.f('ix_stations_name'), 'stations',
                    ['name'], unique=True)

    op.create_table(
        'stations_sensors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('station_id', sa.Integer(), nullable=False),
        sa.Column('sensor_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ),
        sa.ForeignKeyConstraint(['station_id'], ['stations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('station_id', 'sensor_id',
                            name='uq_stations_sensors_station_sensor')
    )
    op.create_index(op.f('ix_stations_sensors_sensor_id'), 'stations_sensors',
                    ['sensor_id'], unique=False)
    op.create_index(op.f('ix_stations_sensors_station_id'), 'stations_sensors',
                    ['station_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_stations_sensors_station_id'),
                  table_name='stations_sensors')
    op.drop_index(op.f('ix_stations_sensors_sensor_id'),
                  table_name='stations_sensors')
    op.drop_table('stations_sensors')

    op.drop_index(op.f('ix_stations_name'), table_name='stations')
    op.drop_index(op.f('ix_stations_location'), table_name='stations')
    op.drop_index(op.f('ix_stations_kind'), table_name='stations')
    op.drop_index(op.f('ix_stations_code'), table_name='stations')
    op.drop_table('stations')
