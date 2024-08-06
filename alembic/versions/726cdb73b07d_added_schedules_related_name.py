"""added_schedules_related_name

Revision ID: 726cdb73b07d
Revises: be093d7d997d
Create Date: 2024-08-05 18:21:09.301928

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '726cdb73b07d'
down_revision: Union[str, None] = 'be093d7d997d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedules', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'schedules', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_column('schedules', 'owner_id')
    # ### end Alembic commands ###