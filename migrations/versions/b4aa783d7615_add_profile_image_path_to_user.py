"""Add profile_image_path to user

Revision ID: b4aa783d7615
Revises: 
Create Date: 2026-01-03 17:51:40.453185

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b4aa783d7615'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('profile_image_path', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'profile_image_path')