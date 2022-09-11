"""add user table

Revision ID: 184d40a8b67b
Revises: 3ffc1a29a06b
Create Date: 2022-09-11 11:10:06.926787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '184d40a8b67b'
down_revision = '3ffc1a29a06b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_column('users')
    pass
