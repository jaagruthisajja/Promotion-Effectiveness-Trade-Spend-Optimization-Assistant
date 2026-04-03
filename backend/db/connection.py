from __future__ import annotations

import os
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = BASE_DIR / "backend" / "db" / "promotion_optimization.db"


def get_database_path() -> Path:
    configured = os.getenv("PROMOTION_DB_PATH")
    return Path(configured) if configured else DEFAULT_DB_PATH


def get_connection() -> sqlite3.Connection:
    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        table_check = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'promotions'"
        ).fetchone()
        if table_check:
            return

        schema_sql = (BASE_DIR / "backend" / "db" / "schema.sql").read_text(encoding="utf-8")
        seed_sql = (BASE_DIR / "backend" / "db" / "sample_data.sql").read_text(encoding="utf-8")
        connection.executescript(schema_sql)
        connection.executescript(seed_sql)
