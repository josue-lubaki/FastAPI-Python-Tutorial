"""add content column to post table

Revision ID: 65cb39d9dd39
Revises: e51a3d2dd329
Create Date: 2022-01-08 23:41:04.147825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65cb39d9dd39'
down_revision = 'e51a3d2dd329'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
