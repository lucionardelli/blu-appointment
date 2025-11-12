from __future__ import annotations

import shutil
import typing as t
from datetime import UTC, datetime
from pathlib import Path

if t.TYPE_CHECKING:
    import logging


def backup_database(db_path: str, logger: logging.Logger, backup_name: str | None = None) -> Path | None:
    """Creates a backup of the database file."""
    p_db_path = Path(db_path)

    if not p_db_path.exists():
        logger.warning(f"Database file not found at {db_path}. Skipping backup.")
        return

    backup_dir = p_db_path.parent

    if backup_name:
        backup_path = backup_dir / backup_name
    else:
        db_filename = p_db_path.name
        backup_path = backup_dir / f"{db_filename}.{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}.bak"

    logger.info(f"Backing up database to {backup_path}...")
    shutil.copy(db_path, backup_path)
    if backup_path.exists():
        logger.info("Backup created successfully.")
        return backup_path
    logger.error("Failed to create database backup.")
    return None
