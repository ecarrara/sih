# -*- coding: utf-8 -*-
"""sources

Revision ID: 4a9f05b93601
Revises: 326bc94b1ca2
Create Date: 2015-09-13 08:17:13.941606

"""

# revision identifiers, used by Alembic.
revision = '4a9f05b93601'
down_revision = '326bc94b1ca2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('identifier', sa.String(length=32), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('url', sa.String(length=255), nullable=True),
        sa.Column('license', sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('identifier')
    )


def downgrade():
    op.drop_table('sources')
