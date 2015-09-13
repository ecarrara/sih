"""cities

Revision ID: 714115f5625
Revises: 16d37adbbe5
Create Date: 2015-09-13 11:29:31.579493

"""

# revision identifiers, used by Alembic.
revision = '714115f5625'
down_revision = '16d37adbbe5'

from alembic import op
from geoalchemy2.types import Geography
import sqlalchemy as sa


def upgrade():
    op.execute('CREATE EXTENSION postgis')
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('state', sa.String(length=2), nullable=False),
        sa.Column('boundary', Geography('POLYGON'), nullable=True),
        sa.Column('center', Geography('POINT'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cities_boundary'), 'cities', ['boundary'],
                    unique=False)
    op.create_index(op.f('ix_cities_center'), 'cities', ['center'],
                    unique=False)


def downgrade():
    op.drop_index(op.f('ix_cities_center'), table_name='cities')
    op.drop_index(op.f('ix_cities_boundary'), table_name='cities')
    op.drop_table('cities')
    op.execute('DROP EXTENSION postgis')
