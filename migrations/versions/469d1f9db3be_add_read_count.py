"""add read count

Revision ID: 469d1f9db3be
Revises: 682ced663f1e
Create Date: 2016-12-29 16:45:43.284000

"""

# revision identifiers, used by Alembic.
revision = '469d1f9db3be'
down_revision = '682ced663f1e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('read_count', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'read_count')
    ### end Alembic commands ###