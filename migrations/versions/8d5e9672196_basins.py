# -*- coding: utf-8 -*-
"""basins

Revision ID: 8d5e9672196
Revises: 191ff53fa59a
Create Date: 2015-09-27 09:32:24.831528

"""

# revision identifiers, used by Alembic.
revision = '8d5e9672196'
down_revision = '191ff53fa59a'

from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geography


def upgrade():
    op.create_table(
        'basins',
        sa.Column('ottocode', sa.String(length=12), nullable=False),
        sa.Column('boundary', Geography('POLYGON'), nullable=True),
        sa.PrimaryKeyConstraint('ottocode')
    )
    op.create_index(op.f('ix_basins_boundary'), 'basins',
                    ['boundary'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_basins_boundary'), table_name='basins')
    op.drop_table('basins')
