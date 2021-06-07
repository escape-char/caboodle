"""create collection bookmark table

Revision ID: 873d38b9d3e5
Revises: 9e25beaabd01
Create Date: 2021-04-15 03:12:59.832386

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow

# revision identifiers, used by Alembic.
revision = '873d38b9d3e5'
down_revision = '9e25beaabd01'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "collection_bookmark"


def upgrade():
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'collection_id',
            sa.Integer,
            sa.ForeignKey('collections.id'),
            index=True
        ),
        sa.Column(
            'bookmark_id',
            sa.Integer,
            sa.ForeignKey('bookmarks.id'),
            index=True
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
