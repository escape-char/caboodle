"""create user role  table

Revision ID: 32e134eed18d
Revises: 725f2e0feef3
Create Date: 2021-04-15 00:49:56.438068

"""
from typing import Final, List
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow, map_timestamp
from backend.settings import settings
from backend.alembic.utils import get_user_roles


# revision identifiers, used by Alembic.
revision = '32e134eed18d'
down_revision = '725f2e0feef3'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "user_role"
USERS_QUERY: Final[str] = (
    "SELECT id, username FROM users WHERE username=:username"
)
ROLES_QUERY: Final[str] = "SELECT id, name FROM roles"


def upgrade():
    table = op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'user_id',
            sa.Integer,
            sa.ForeignKey('users.id'),
            index=True,
            nullable=False
        ),
        sa.Column(
            'role_id',
            sa.Integer,
            sa.ForeignKey('roles.id'),
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
    res = conn.execute(
        sa.text(USERS_QUERY),
        {"username": settings.default_admin_username}
    )
    users = res.fetchall()
    users = [dict(u) for u in users]

    print("users: ", users)

    res = conn.execute(ROLES_QUERY)
    roles = res.fetchall()
    roles = [dict(r) for r in roles]

    user_roles: List[dict] = get_user_roles(users[0], roles)
    user_roles = map_timestamp(user_roles)

    op.bulk_insert(table, user_roles)


def downgrade():
    op.drop_table(TABLE_NAME)
