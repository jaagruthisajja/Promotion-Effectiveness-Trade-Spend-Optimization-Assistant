from __future__ import annotations

import re

from backend.db.schema_metadata import APPROVED_TABLES


FORBIDDEN_KEYWORDS = (
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "EXEC",
    "CREATE",
)


def validate_sql(sql: str, limit: int = 100) -> dict:
    normalized = sql.strip().rstrip(";")
    upper_sql = normalized.upper()

    if not upper_sql.startswith("SELECT"):
        return {"is_valid": False, "sql": normalized, "reason": "Only SELECT queries are allowed."}

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            return {
                "is_valid": False,
                "sql": normalized,
                "reason": f"Forbidden SQL keyword detected: {keyword}.",
            }

    table_references = {
        match.lower()
        for match in re.findall(r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)", normalized, re.IGNORECASE)
    }
    if not table_references.issubset(APPROVED_TABLES):
        invalid_tables = ", ".join(sorted(table_references - APPROVED_TABLES))
        return {
            "is_valid": False,
            "sql": normalized,
            "reason": f"Query references non-approved tables: {invalid_tables}.",
        }

    if not re.search(r"\bLIMIT\s+\d+\b", upper_sql):
        normalized = f"{normalized}\nLIMIT {limit}"

    return {"is_valid": True, "sql": normalized, "reason": None}
