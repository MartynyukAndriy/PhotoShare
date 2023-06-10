"""Init

Revision ID: d2bb63b969a7
Revises: 
Create Date: 2023-06-09 09:32:11.511342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2bb63b969a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('picture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=300), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_picture_id'), 'picture', ['id'], unique=False)
    op.create_index(op.f('ix_picture_url'), 'picture', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_picture_url'), table_name='picture')
    op.drop_index(op.f('ix_picture_id'), table_name='picture')
    op.drop_table('picture')
    # ### end Alembic commands ###
