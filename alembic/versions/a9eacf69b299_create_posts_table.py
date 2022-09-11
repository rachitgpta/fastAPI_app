"""create posts table

Revision ID: a9eacf69b299
Revises: 
Create Date: 2022-08-28 23:04:47.345730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9eacf69b299'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('title', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    pass
