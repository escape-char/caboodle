"""create collections table

Revision ID: 9e25beaabd01
Revises: b978ac64a6f9
Create Date: 2021-04-15 03:05:57.387019

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow


# revision identifiers, used by Alembic.
revision = '9e25beaabd01'
down_revision = 'b978ac64a6f9'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "collections"


def upgrade():
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'user_id',
            sa.Integer,
            sa.ForeignKey('users.id'),
            index=True
        ),
        sa.Column(
            'name',
            sa.String(60),
            nullable=False
        ),
        sa.Column(
            'count',
            sa.Integer,
            nullable=False,
            default=0
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
