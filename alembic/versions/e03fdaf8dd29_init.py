"""init

Revision ID: e03fdaf8dd29
Revises: 
Create Date: 2024-08-30 18:21:15.309659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e03fdaf8dd29'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer_transaction_requests',
    sa.Column('request_id', sa.String(), nullable=False),
    sa.Column('customer_id', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('request_id')
    )
    op.create_index(op.f('ix_customer_transaction_requests_customer_id'), 'customer_transaction_requests', ['customer_id'], unique=False)
    op.create_index(op.f('ix_customer_transaction_requests_request_id'), 'customer_transaction_requests', ['request_id'], unique=False)
    op.create_table('transactions',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('request_id', sa.String(), nullable=False),
    sa.Column('customer_id', sa.BigInteger(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('bank', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('phone_number', sa.String(length=11), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=True),
    sa.Column('password', sa.String(length=1024), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=False),
    sa.Column('last_name', sa.String(length=256), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_customer_transaction_requests_request_id'), table_name='customer_transaction_requests')
    op.drop_index(op.f('ix_customer_transaction_requests_customer_id'), table_name='customer_transaction_requests')
    op.drop_table('customer_transaction_requests')
    # ### end Alembic commands ###
