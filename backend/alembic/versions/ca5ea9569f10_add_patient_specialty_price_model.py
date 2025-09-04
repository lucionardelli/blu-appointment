"""add patient_specialty_price model

Revision ID: ca5ea9569f10
Revises: eb9df48a6336
Create Date: 2025-09-03 20:44:34.842954

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ca5ea9569f10"
down_revision: str | Sequence[str] | None = "eb9df48a6336"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "patient_specialty_prices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("specialty_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["specialty_id"], ["specialties.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("patient_id", "specialty_id", name="uq_patient_specialty_price"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("patient_specialty_prices")
