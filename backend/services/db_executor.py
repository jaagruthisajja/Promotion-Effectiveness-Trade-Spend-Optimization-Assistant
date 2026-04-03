from __future__ import annotations

from backend.db.connection import get_connection


def execute_query(sql: str) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(sql).fetchall()
    return [dict(row) for row in rows]
