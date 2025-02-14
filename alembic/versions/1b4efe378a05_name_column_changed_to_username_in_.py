"""name column changed to username in company model

Revision ID: 1b4efe378a05
Revises: 914e75ba4fde
Create Date: 2025-02-14 21:51:02.645973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1b4efe378a05'
down_revision: Union[str, None] = '914e75ba4fde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('username', sa.String(length=50), nullable=False))
    op.drop_column('companies', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('name', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('companies', 'username')
    # ### end Alembic commands ###
