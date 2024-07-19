"""create ai_providers table

Revision ID: 4aea7791fbf6
Revises: 
Create Date: 2024-07-19 12:54:01.882577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aea7791fbf6'
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ai_providers_name'), table_name='ai_providers')
    op.drop_table('ai_providers')
    # ### end Alembic commands ###
