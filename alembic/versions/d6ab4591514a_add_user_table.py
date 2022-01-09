"""add user table

Revision ID: d6ab4591514a
Revises: 65cb39d9dd39
Create Date: 2022-01-08 23:46:04.565923

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'd6ab4591514a'
down_revision = '65cb39d9dd39'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('email', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=text('NOW()'), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
