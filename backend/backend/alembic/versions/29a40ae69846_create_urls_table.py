"""create urls table

Revision ID: 29a40ae69846
Revises: 32e134eed18d
Create Date: 2021-04-15 01:44:19.365765

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow

# revision identifiers, used by Alembic.
revision = '29a40ae69846'
down_revision = '32e134eed18d'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "urls"


def upgrade():
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'url',
            sa.Text,
            nullable=False,
            unique=True,
            index=True
        ),
        sa.Column(
            'domain',
            sa.String(255),
            nullable=False,
            index=True
        ),
        sa.Column(
            'last_checked',
            sa.DateTime,
            nullable=True,
            default=None
        ),
        sa.Column(
            'http_status',
            sa.SmallInteger,
            nullable=True,
            default=None
        ),
        sa.Column(
            'http_last_modified',
            sa.DateTime,
            nullable=True,
            default=None
        ),
        sa.Column(
            'content_hash',
            sa.String(255),
            nullable=True,
            default=None
        ),
        sa.Column(
            'http_etag',
            sa.String(255),
            nullable=True,
            default=None
        ),
        sa.Column(
            'count',
            sa.Integer,
            nullable=False,
            default=0
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


def downgrade():
    op.drop_table(TABLE_NAME)
