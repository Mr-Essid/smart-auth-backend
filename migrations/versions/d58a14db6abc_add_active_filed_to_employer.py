"""add active filed to employer

Revision ID: d58a14db6abc
Revises: 26e1ff499f2b
Create Date: 2023-12-21 00:43:49.566187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd58a14db6abc'
down_revision: Union[str, None] = '26e1ff499f2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
