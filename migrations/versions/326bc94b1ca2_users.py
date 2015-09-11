# -*- coding: utf-8 -*-
"""users

Revision ID: 326bc94b1ca2
Revises: None
Create Date: 2015-09-11 18:25:05.178387

"""

# revision identifiers, used by Alembic.
revision = '326bc94b1ca2'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=32), nullable=False),
        sa.Column('roles', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', name='user_status'),
                  nullable=False),
        sa.Column('api_key', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )


def downgrade():
    op.drop_table('users')
