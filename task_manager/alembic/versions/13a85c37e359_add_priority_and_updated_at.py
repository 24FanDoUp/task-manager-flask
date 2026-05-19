"""add priority and updated_at

Revision ID: 13a85c37e359
Revises: c08d7f19991e
Create Date: 2026-05-17 11:44:48.908311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '13a85c37e359'
down_revision: Union[str, Sequence[str], None] = 'c08d7f19991e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "tasks",
        sa.Column("priority",sa.String(), nullable= True)
    )
    op.add_column(
        "tasks",
        sa.Column("updated_at",sa.DateTime(),nullable=True)
    )
    
    op.execute("UPDATE tasks SET priority = 'Medium' WHERE priority is NULL ")
    op.execute("UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE updated_at is NULL ")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tasks","updated_at")
    op.drop_column("tasks","priority")
