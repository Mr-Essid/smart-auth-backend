"""create admin table

Revision ID: f0a2f555a8cb
Revises: 
Create Date: 2023-12-16 18:09:39.523648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0a2f555a8cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id_admin', sa.Integer(), sa.Identity(always=False, start=1), nullable=False),
    sa.Column('name_admin', sa.String(length=30), nullable=False),
    sa.Column('email_admin', sa.String(length=100), nullable=False),
    sa.Column('password_admin', sa.String(length=100), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('create_at', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id_admin'),
    sa.UniqueConstraint('email_admin')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admins')
    # ### end Alembic commands ###