from __future__ import annotations

from backend.db.schema_metadata import SCHEMA_METADATA


INTENT_PRIORITIES = {
    "find_top_performer": ("promotion_performance", "promotions", "products", "regions", "channels"),
    "find_low_performing_promotions": (
        "promotion_performance",
        "promotions",
        "products",
        "regions",
        "channels",
    ),
    "find_high_spend_low_performance": (
        "promotions",
        "promotion_performance",
        "products",
        "regions",
        "channels",
    ),
    "find_highest_trade_spend": ("promotions", "products", "regions", "channels"),
    "recommend_budget_reduction": (
        "promotion_performance",
        "promotions",
        "products",
        "regions",
        "channels",
    ),
}


def retrieve_schema_context(extracted_query: dict) -> list[dict]:
    ranked_tables = []
    priorities = INTENT_PRIORITIES.get(extracted_query["intent"], tuple(SCHEMA_METADATA.keys()))

    for index, table_name in enumerate(priorities, start=1):
        table = SCHEMA_METADATA[table_name]
        ranked_tables.append(
            {
                "rank": index,
                "table": table_name,
                "description": table["description"],
                "columns": table["columns"],
            }
        )

    return ranked_tables
