"""disentangle payments from method and use payment_method_id

Revision ID: 5b6e2d0b822f
Revises: 06fea00a2b97
Create Date: 2025-08-20 19:32:47.522346

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5b6e2d0b822f"
down_revision: str | Sequence[str] | None = "06fea00a2b97"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_table("payments")
    # Create new table with updated schema
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("payment_date", sa.DateTime(), nullable=False),
        sa.Column("payment_method_id", sa.Integer(), sa.ForeignKey("payment_methods.id"), nullable=False),
        sa.Column("appointment_id", sa.Integer(), sa.ForeignKey("appointments.id"), nullable=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.id"), nullable=False),
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)


def downgrade() -> None:
    # Recreate original table with 'method' column and without new FKs
    op.drop_table("payments")
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("payment_date", sa.DateTime(), nullable=False),
        sa.Column("appointment_id", sa.Integer(), sa.ForeignKey("appointments.id"), nullable=False),
        sa.Column("method", sa.String(length=14), nullable=False),
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
