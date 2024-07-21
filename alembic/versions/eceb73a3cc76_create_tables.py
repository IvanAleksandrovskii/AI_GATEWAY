"""create tables

Revision ID: eceb73a3cc76
Revises: 
Create Date: 2024-07-20 20:48:33.656518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eceb73a3cc76'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ai_providers',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('api_url', sa.String(), nullable=True),
    sa.Column('api_key', sa.String(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_providers_name'), 'ai_providers', ['name'], unique=True)
    op.create_table('tokens',
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_token'), 'tokens', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tokens_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_ai_providers_name'), table_name='ai_providers')
    op.drop_table('ai_providers')
    # ### end Alembic commands ###