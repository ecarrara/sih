# -*- coding: utf-8 -*-
"""data

Revision ID: 191ff53fa59a
Revises: 434bd1991540
Create Date: 2015-09-15 19:41:52.610013

"""

revision = '191ff53fa59a'
down_revision = '434bd1991540'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('received_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('station_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['station_id'], ['stations.id'],
                                onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('station_id', 'read_at',
                            name='uq_data_station_id_read_at')
    )
    op.create_index(op.f('ix_data_read_at'), 'data',
                    ['read_at'], unique=False)
    op.create_index(op.f('ix_data_station_id'), 'data',
                    ['station_id'], unique=False)

    op.create_table(
        'sensor_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_id', sa.Integer(), nullable=False),
        sa.Column('sensor_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['data_id'], ['data.id'],
                                onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'],
                                onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('data_id', 'sensor_id',
                            name='uq_sensor_data_data_id_sensor_id')
    )
    op.create_index(op.f('ix_sensor_data_data_id'), 'sensor_data',
                    ['data_id'], unique=False)
    op.create_index(op.f('ix_sensor_data_sensor_id'), 'sensor_data',
                    ['sensor_id'], unique=False)
    op.create_index(op.f('ix_sensor_data_value'), 'sensor_data',
                    ['value'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_sensor_data_value'), table_name='sensor_data')
    op.drop_index(op.f('ix_sensor_data_sensor_id'), table_name='sensor_data')
    op.drop_index(op.f('ix_sensor_data_data_id'), table_name='sensor_data')
    op.drop_table('sensor_data')

    op.drop_index(op.f('ix_data_station_id'), table_name='data')
    op.drop_index(op.f('ix_data_read_at'), table_name='data')
    op.drop_table('data')
