"""Add task log api field

Revision ID: 874ba5e5da44
Revises: c773a35c280f
Create Date: 2022-02-03 16:22:37.506019

"""
import sqlalchemy as sa
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import engine_from_config
from sqlalchemy.engine import reflection

revision = '874ba5e5da44'
down_revision = 'c773a35c280f'
branch_labels = None
depends_on = None


def upgrade():
    # Issue changes on existing user activities table and migrate existing rows
    # Add column is_from_api to user_activities if not existing and set existing ones to false
    if not _table_has_column('user_activity', 'is_from_api'):
        op.add_column('user_activity',
                      sa.Column('is_from_api', sa.Boolean)
                      )

        t_ua = sa.Table(
            'user_activity',
            sa.MetaData(),
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('is_from_api', sa.Boolean)
        )
        conn = op.get_bind()
        conn.execute(t_ua.update().values(
            is_from_api=False
        ))

    pass


def downgrade():
    pass


def _table_has_column(table, column):
    config = op.get_context().config
    engine = engine_from_config(
        config.get_section(config.config_ini_section), prefix='sqlalchemy.')
    insp = reflection.Inspector.from_engine(engine)
    has_column = False

    for col in insp.get_columns(table):
        if column != col['name']:
            continue
        has_column = True
    return has_column