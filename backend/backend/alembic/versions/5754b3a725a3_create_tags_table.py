"""create tags table

Revision ID: 5754b3a725a3
Revises: 873d38b9d3e5
Create Date: 2021-04-15 03:18:05.557610

"""
from typing import Final
from alembic import op
import sqlalchemy as sa
from backend.common.utils import utcnow


# revision identifiers, used by Alembic.
revision = '5754b3a725a3'
down_revision = '873d38b9d3e5'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "tags"


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
