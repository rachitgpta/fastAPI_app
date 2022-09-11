"""add foreign table to post table

Revision ID: 01eac9a6ac2b
Revises: 184d40a8b67b
Create Date: 2022-09-11 11:15:46.543866

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '01eac9a6ac2b'
down_revision = '184d40a8b67b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_FK', source_table='posts', referent_table="users", local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_FK', table_name="posts")
    op.drop_column(table_name='posts',column_name= 'owner_id')
    pass
