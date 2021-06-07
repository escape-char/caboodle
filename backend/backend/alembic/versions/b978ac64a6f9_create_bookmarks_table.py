"""create bookmarks table

Revision ID: b978ac64a6f9
Revises: 0b05c6a4c96e
Create Date: 2021-04-15 02:49:02.383418

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow

# revision identifiers, used by Alembic.
revision = 'b978ac64a6f9'
down_revision = '0b05c6a4c96e'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "bookmarks"


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
            'user_id',
            sa.Integer,
            sa.ForeignKey('users.id'),
            index=True
        ),
        sa.Column(
            'title',
            sa.String(255),
            nullable=False
        ),
        sa.Column(
            'description',
            sa.Text,
            nullable=False
        ),
        sa.Column(
            'image_path',
            sa.String(255),
            nullable=True
        ),
        sa.Column(
            'snapshot_id',
            sa.Integer,
            sa.ForeignKey('snapshots.id'),
            nullable=True
        ),
        sa.Column(
            'to_read',
            sa.Boolean,
            nullable=False,
            default=False
        ),
        sa.Column(
            'favorite',
            sa.Boolean,
            nullable=False,
            default=False
        ),
        sa.Column(
            'private',
            sa.Boolean,
            nullable=False,
            default=False
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
