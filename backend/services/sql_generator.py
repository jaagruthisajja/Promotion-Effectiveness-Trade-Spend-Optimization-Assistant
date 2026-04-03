from __future__ import annotations

from typing import Any


SELECT_FIELDS = {
    "roi": "pp.roi",
    "sales_lift_percent": "pp.sales_lift_percent",
    "spend_efficiency": "ROUND(pp.incremental_sales / NULLIF(p.trade_spend, 0), 2)",
    "incremental_sales": "pp.incremental_sales",
    "trade_spend": "p.trade_spend",
}


GROUP_BY_FIELDS = {
    "brand": ("pr.brand", "brand"),
    "category": ("pr.category", "category"),
    "region": ("r.region_name", "region"),
    "channel": ("c.channel_name", "channel"),
    "promotion_name": ("p.promotion_name", "promotion_name"),
    "promotion_type": ("p.promotion_type", "promotion_type"),
}


def _base_from_clause() -> str:
    return """
FROM promotions p
JOIN promotion_performance pp ON p.promotion_id = pp.promotion_id
JOIN products pr ON p.product_id = pr.product_id
JOIN regions r ON p.region_id = r.region_id
JOIN channels c ON p.channel_id = c.channel_id
""".strip()


def _build_where(filters: dict[str, Any]) -> str:
    conditions: list[str] = []
    if filters.get("brand"):
        conditions.append(f"pr.brand = '{filters['brand']}'")
    if filters.get("category"):
        conditions.append(f"pr.category = '{filters['category']}'")
    if filters.get("region"):
        conditions.append(f"r.region_name = '{filters['region']}'")
    if filters.get("channel"):
        conditions.append(f"c.channel_name = '{filters['channel']}'")
    if filters.get("promotion_type"):
        conditions.append(f"p.promotion_type = '{filters['promotion_type']}'")
    if filters.get("time_period"):
        period = filters["time_period"]
        conditions.append(
            f"p.start_date <= '{period['end_date']}' AND p.end_date >= '{period['start_date']}'"
        )
    return "" if not conditions else "WHERE " + " AND ".join(conditions)


def _order_for_intent(intent: str, metric: str) -> str:
    metric_expression = SELECT_FIELDS[metric]
    if intent in {"find_top_performer", "find_highest_trade_spend"}:
        return f"ORDER BY {metric_expression} DESC"
    if intent in {
        "find_low_performing_promotions",
        "find_high_spend_low_performance",
        "recommend_budget_reduction",
    }:
        if metric == "trade_spend":
            return "ORDER BY p.trade_spend DESC, pp.roi ASC"
        return f"ORDER BY {metric_expression} ASC"
    return "ORDER BY p.start_date DESC"


def generate_sql(user_query: str, extracted_query: dict, schema_context: list[dict], metric_formulas: dict) -> str:
    del user_query, schema_context, metric_formulas

    filters = extracted_query["filters"]
    metric = extracted_query["metric"] or "roi"
    intent = extracted_query["intent"]
    group_by = extracted_query.get("group_by")
    where_clause = _build_where(filters)

    if group_by in GROUP_BY_FIELDS:
        group_field, alias = GROUP_BY_FIELDS[group_by]
        metric_expression = SELECT_FIELDS[metric]
        direction = "ASC" if ("low" in intent or "reduction" in intent) else "DESC"
        return f"""
SELECT
    {group_field} AS {alias},
    ROUND(AVG({metric_expression}), 2) AS metric_value,
    ROUND(SUM(pp.incremental_sales), 2) AS incremental_sales,
    ROUND(SUM(p.trade_spend), 2) AS trade_spend
{_base_from_clause()}
{where_clause}
GROUP BY {group_field}
ORDER BY metric_value {direction}
LIMIT 10
""".strip()

    metric_expression = SELECT_FIELDS[metric]
    return f"""
SELECT
    p.promotion_id,
    p.promotion_name,
    p.promotion_type,
    pr.product_name,
    pr.brand,
    pr.category,
    r.region_name AS region,
    c.channel_name AS channel,
    p.start_date,
    p.end_date,
    ROUND(p.trade_spend, 2) AS trade_spend,
    ROUND(pp.baseline_sales, 2) AS baseline_sales,
    ROUND(pp.promoted_sales, 2) AS promoted_sales,
    ROUND(pp.incremental_sales, 2) AS incremental_sales,
    ROUND(pp.roi, 2) AS roi,
    ROUND(pp.sales_lift_percent, 2) AS sales_lift_percent,
    ROUND(pp.incremental_sales / NULLIF(p.trade_spend, 0), 2) AS spend_efficiency,
    ROUND({metric_expression}, 2) AS metric_value
{_base_from_clause()}
{where_clause}
{_order_for_intent(intent, metric)}
LIMIT 10
""".strip()
