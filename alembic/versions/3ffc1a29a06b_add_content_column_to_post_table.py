"""add content column to post table

Revision ID: 3ffc1a29a06b
Revises: a9eacf69b299
Create Date: 2022-09-10 16:08:05.729649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ffc1a29a06b'
down_revision = 'a9eacf69b299'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
