"""Initial migration

Revision ID: 5159b42a91dc
Revises: 
Create Date: 2024-11-15 13:40:42.337974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5159b42a91dc'
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
