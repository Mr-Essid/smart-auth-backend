"""message

Revision ID: 3ccbd002fd09
Revises: 847c20a84fba
Create Date: 2023-12-25 14:59:18.618464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ccbd002fd09'
down_revision: Union[str, None] = '847c20a84fba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admins', sa.Column('authority', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admins', 'authority')
    # ### end Alembic commands ###
