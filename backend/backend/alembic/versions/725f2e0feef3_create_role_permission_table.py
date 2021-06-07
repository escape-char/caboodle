"""create role permission table

Revision ID: 725f2e0feef3
Revises: df96d01155f3
Create Date: 2021-04-14 19:33:35.311346

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow, map_timestamp
from backend.alembic.utils import get_role_perm

# revision identifiers, used by Alembic.
revision = '725f2e0feef3'
down_revision = 'df96d01155f3'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "role_permission"
QUERY: Final[str] = (
    "SELECT roles.resource_id, json_agg(distinct roles.*) AS roles,"
    "json_agg(DISTINCT permissions.*) AS permissions "
    "FROM roles INNER JOIN permissions ON "
    "permissions.resource_id = roles.resource_id GROUP BY roles.resource_id"
)


def upgrade():
    table = op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'role_id',
            sa.Integer,
            sa.ForeignKey('roles.id'),
            index=True,
            nullable=False
        ),
        sa.Column(
            'permission_id',
            sa.Integer,
            sa.ForeignKey('permissions.id'),
            index=True,
            nullable=False
        ),
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

    role_perm = get_role_perm(results)
    role_perm = map_timestamp(role_perm)

    op.bulk_insert(table, role_perm)


def downgrade():
    op.drop_table(TABLE_NAME)
