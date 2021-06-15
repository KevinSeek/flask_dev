"""empty message

Revision ID: 0bfa81661947
Revises: 66d270f0b308
Create Date: 2021-06-15 20:43:13.766846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bfa81661947'
down_revision = '66d270f0b308'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('location', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'about_me')
    op.drop_column('users', 'location')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###
