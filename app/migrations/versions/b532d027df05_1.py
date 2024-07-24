"""1

Revision ID: b532d027df05
Revises: e51fff3762b4
Create Date: 2024-07-22 21:31:46.099022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b532d027df05'
down_revision: Union[str, None] = 'e51fff3762b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('is_developer', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('is_user', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_user')
    op.drop_column('user', 'is_developer')
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###
