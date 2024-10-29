"""Initial migration

Revision ID: 233f5f6b9ff7
Revises: 
Create Date: 2024-10-29 00:05:13.256069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '233f5f6b9ff7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('idea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('votes', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('idea')
    # ### end Alembic commands ###