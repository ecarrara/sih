# -*- coding: utf-8 -*-
"""sensors

Revision ID: 16d37adbbe5
Revises: 4a9f05b93601
Create Date: 2015-09-13 09:45:13.819141

"""

# revision identifiers, used by Alembic.
revision = '16d37adbbe5'
down_revision = '4a9f05b93601'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'sensors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('identifier', sa.String(length=32), nullable=False),
        sa.Column('measure_unit', sa.String(length=32), nullable=False),
        sa.Column('validate_code', sa.Text(), nullable=True),
        sa.Column('process_code', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('identifier')
    )


def downgrade():
    op.drop_table('sensors')
