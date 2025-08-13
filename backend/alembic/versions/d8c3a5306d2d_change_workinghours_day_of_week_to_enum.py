"""Change WorkingHours day_of_week to Enum

Revision ID: d8c3a5306d2d
Revises: bae93f23d644
Create Date: 2025-08-13 18:50:13.773736

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8c3a5306d2d"
down_revision: str | Sequence[str] | None = "bae93f23d644"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("PRAGMA foreign_keys=OFF;")
    op.execute(
        """
        CREATE TABLE working_hours_new (
            id INTEGER NOT NULL,
            day_of_week VARCHAR(255) NOT NULL,
            start_time TIME WITHOUT TIME ZONE NOT NULL,
            end_time TIME WITHOUT TIME ZONE NOT NULL,
            is_closed BOOLEAN NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    op.execute(
        """
        INSERT INTO working_hours_new (id, day_of_week, start_time, end_time, is_closed)
        SELECT id,
               CASE day_of_week
                   WHEN 0 THEN 'MONDAY'
                   WHEN 1 THEN 'TUESDAY'
                   WHEN 2 THEN 'WEDNESDAY'
                   WHEN 3 THEN 'THURSDAY'
                   WHEN 4 THEN 'FRIDAY'
                   WHEN 5 THEN 'SATURDAY'
                   WHEN 6 THEN 'SUNDAY'
               END,
               start_time,
               end_time,
               is_closed
        FROM working_hours;
        """
    )
    op.execute("DROP TABLE working_hours;")
    op.execute("ALTER TABLE working_hours_new RENAME TO working_hours;")
    op.execute("PRAGMA foreign_keys=ON;")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("PRAGMA foreign_keys=OFF;")
    op.execute(
        """
        CREATE TABLE working_hours_new (
            id INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            start_time TIME WITHOUT TIME ZONE NOT NULL,
            end_time TIME WITHOUT TIME ZONE NOT NULL,
            is_closed BOOLEAN NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    op.execute(
        """
        INSERT INTO working_hours_new (id, day_of_week, start_time, end_time, is_closed)
        SELECT id,
               CASE day_of_week
                   WHEN 'MONDAY' THEN 0
                   WHEN 'TUESDAY' THEN 1
                   WHEN 'WEDNESDAY' THEN 2
                   WHEN 'THURSDAY' THEN 3
                   WHEN 'FRIDAY' THEN 4
                   WHEN 'SATURDAY' THEN 5
                   WHEN 'SUNDAY' THEN 6
               END,
               start_time,
               end_time,
               is_closed
        FROM working_hours;
        """
    )
    op.execute("DROP TABLE working_hours;")
    op.execute("ALTER TABLE working_hours_new RENAME TO working_hours;")
    op.execute("PRAGMA foreign_keys=ON;")
