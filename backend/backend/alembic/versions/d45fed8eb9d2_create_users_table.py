"""create users table

Revision ID: d45fed8eb9d2
Revises:
Create Date: 2021-04-09 11:26:00.627136

"""
from typing import Final
from alembic import op
import sqlalchemy as sa

from backend.settings import settings
from backend.common.security.utils import (gen_password_hash)
from backend.common.utils import (utcnow)


# revision identifiers, used by Alembic.
revision = 'd45fed8eb9d2'
down_revision = None
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "users"


def upgrade():
    table = op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'username',
            sa.String(45),
            nullable=False,
            unique=True,
            index=True
        ),
        sa.Column('password', sa.String(70), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=True, default=""),
        sa.Column('name', sa.String(70), nullable=False),
        sa.Column('dark_theme', sa.Boolean, default=False),
        sa.Column('retries', sa.SmallInteger, nullable=False, default=0),
        sa.Column('locked_until', sa.DateTime, nullable=True, default=None),
        sa.Column(
            'last_login',
            sa.DateTime,
            nullable=True,
            default=None
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

    # create default admin user
    op.bulk_insert(table, [{
        'username': settings.default_admin_username,
        'password': gen_password_hash(settings.default_admin_password),
        'email': settings.default_admin_email,
        'name': settings.default_admin_name,
        'created_at': utcnow(),
        'modified_at': utcnow()
    }])


def downgrade():
    op.drop_table(TABLE_NAME)
