"""create resources table

Revision ID: bb9231b718ca
Revises: d45fed8eb9d2
Create Date: 2021-04-10 10:21:01.276562

"""
from typing import List, Final, Dict
from alembic import op
import sqlalchemy as sa
from backend.alembic.utils import get_resources
from backend.common.utils import map_timestamp, utcnow


# revision identifiers, used by Alembic.
revision = 'bb9231b718ca'
down_revision = 'd45fed8eb9d2'
branch_labels = None
depends_on = None

TABLE_NAME: Final[str] = "resources"


def upgrade():
    table = op.create_table(
            TABLE_NAME,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column(
                'name',
                sa.String(45),
                nullable=False,
                unique=True,
                index=True
            ),
            sa.Column('description', sa.String(150), nullable=False),
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

    resources: Final[List[Dict[str, str]]] = map_timestamp(get_resources())

    # create default resources
    op.bulk_insert(table, resources)


def downgrade():
    op.drop_table(TABLE_NAME)
