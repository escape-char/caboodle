"""create snapshots table

Revision ID: 0b05c6a4c96e
Revises: 29a40ae69846
Create Date: 2021-04-15 02:14:15.824073

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow


# revision identifiers, used by Alembic.
revision = '0b05c6a4c96e'
down_revision = '29a40ae69846'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "snapshots"


def upgrade():
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'url_id',
            sa.Integer,
            sa.ForeignKey('urls.id'),
            index=True
        ),
        sa.Column(
            'crawled_at',
            sa.DateTime,
            nullable=False,
            default=utcnow
        ),
        sa.Column(
            'http_content_type',
            sa.String(255),
            nullable=False,
            index=True
        ),
        sa.Column(
            'http_etag',
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
            'http_content_type',
            sa.String(255),
            nullable=True,
            default=None
        ),
        sa.Column(
            'http_status_code',
            sa.SmallInteger,
            nullable=False,
        ),
        sa.Column(
            'http_content_length',
            sa.Integer,
            nullable=True,
        ),
        sa.Column(
            'file_count',
            sa.Integer,
            default=0
        ),
        sa.Column(
            'size',
            sa.Integer,
            default=0
        ),
        sa.Column(
            'last_snapshot',
            sa.DateTime,
            nullable=True
        ),
        sa.Column(
            'last_url_id',
            sa.Integer,
            sa.ForeignKey('urls.id'),
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


def downgrade():
    op.drop_table(TABLE_NAME)
