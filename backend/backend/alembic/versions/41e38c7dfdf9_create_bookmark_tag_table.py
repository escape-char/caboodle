"""create bookmark tag table

Revision ID: 41e38c7dfdf9
Revises: 5754b3a725a3
Create Date: 2021-04-15 03:24:07.343714

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow


# revision identifiers, used by Alembic.
revision = '41e38c7dfdf9'
down_revision = '5754b3a725a3'
branch_labels = None
depends_on = None


TABLE_NAME: Final[str] = "bookmark_tag"


def upgrade():
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'bookmark_id',
            sa.Integer,
            sa.ForeignKey('bookmarks.id'),
            index=True
        ),
        sa.Column(
            'tag_id',
            sa.Integer,
            sa.ForeignKey('tags.id'),
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
