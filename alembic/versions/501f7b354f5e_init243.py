"""init243

Revision ID: 501f7b354f5e
Revises: e3e6b6663d83
Create Date: 2024-08-30 18:37:55.004569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '501f7b354f5e'
down_revision: Union[str, None] = 'e3e6b6663d83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('bank', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'bank')
    # ### end Alembic commands ###
