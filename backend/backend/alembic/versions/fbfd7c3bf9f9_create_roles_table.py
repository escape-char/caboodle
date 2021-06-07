"""create roles table

Revision ID: fbfd7c3bf9f9
Revises: bb9231b718ca
Create Date: 2021-04-11 12:50:56.735105

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.alembic.utils import get_roles_from_resources
from backend.common.utils import map_timestamp, utcnow


# revision identifiers, used by Alembic.
revision = 'fbfd7c3bf9f9'
down_revision = 'bb9231b718ca'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "roles"


def upgrade():
    QUERY: Final[str] = "SELECT id, name FROM resources"

    table = op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'resource_id',
            sa.Integer,
            sa.ForeignKey('resources.id'),
            index=True,
            nullable=False
        ),
        sa.Column(
            'name',
            sa.String(45),
            nullable=False,
            unique=True,
            index=True
        ),
        sa.Column('description', sa.String(150), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime,
            nullable=False,
            default=utcnow
        ),
        sa.Column(
            'modified_at',
            sa.DateTime,
            nullable=False,
            default=utcnow
        )
    )

    conn = op.get_bind()
    res = conn.execute(QUERY)
    results = res.fetchall()
    results = [dict(r) for r in results]

    roles: list = get_roles_from_resources(results)

    roles_with_ts: list = map_timestamp(roles)

    op.bulk_insert(table, roles_with_ts)


def downgrade():
    op.drop_table(TABLE_NAME)
