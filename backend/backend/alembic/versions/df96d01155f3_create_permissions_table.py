"""create permissions table

Revision ID: df96d01155f3
Revises: fbfd7c3bf9f9
Create Date: 2021-04-12 13:06:13.223999

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import map_timestamp, utcnow
from backend.alembic.utils import get_perms_from_resources


# revision identifiers, used by Alembic.
revision = 'df96d01155f3'
down_revision = 'fbfd7c3bf9f9'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "permissions"

QUERY: Final[str] = "SELECT id, name FROM resources"


def upgrade():
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

    perms: list = get_perms_from_resources(results)
    perms_with_ts: list = map_timestamp(perms)

    op.bulk_insert(table, perms_with_ts)


def downgrade():
    op.drop_table(TABLE_NAME)
