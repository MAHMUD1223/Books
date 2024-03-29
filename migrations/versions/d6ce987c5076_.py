"""empty message

Revision ID: d6ce987c5076
Revises: 
Create Date: 2023-12-19 00:10:26.719721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6ce987c5076'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_name', sa.String(length=80), nullable=False),
    sa.Column('author', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('book', sa.Text(), nullable=False),
    sa.Column('page', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('book_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
