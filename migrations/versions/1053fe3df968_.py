"""empty message

Revision ID: 1053fe3df968
Revises: e717189a2084
Create Date: 2023-09-10 22:17:57.556114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1053fe3df968'
down_revision = 'e717189a2084'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('evidence',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('evidence')
    # ### end Alembic commands ###