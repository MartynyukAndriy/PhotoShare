"""changed transformed image

Revision ID: b7ecc89aa603
Revises: ac6a8e3eb141
Create Date: 2023-06-20 02:35:55.332551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7ecc89aa603'
down_revision = 'ac6a8e3eb141'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transformed_images', sa.Column('qrcode_image_url', sa.String(), nullable=False))
    op.add_column('transformed_images', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transformed_images', 'created_at')
    op.drop_column('transformed_images', 'qrcode_image_url')
    # ### end Alembic commands ###
