from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Catalog:
    brands: tuple[str, ...] = ("GlowCare", "BrightSmile", "CleanWave", "SparkHome")
    categories: tuple[str, ...] = (
        "Shampoos",
        "Oral Care",
        "Bathing",
        "Conditioners",
        "Home Care",
    )
    regions: tuple[str, ...] = ("South India", "West India", "North India", "East India")
    channels: tuple[str, ...] = ("General Trade", "Modern Trade", "E-commerce")
    promotion_types: tuple[str, ...] = (
        "discount",
        "bundle offer",
        "display support",
        "seasonal scheme",
        "cashback",
    )


CATALOG = Catalog()


def _extract_match(query: str, options: tuple[str, ...]) -> str | None:
    lowered = query.lower()
    for option in options:
        if option.lower() in lowered:
            return option
    return None


def _extract_time_period(query: str) -> dict[str, str] | None:
    quarter_match = re.search(r"\bq([1-4])\s+(20\d{2})\b", query, re.IGNORECASE)
    if quarter_match:
        quarter = int(quarter_match.group(1))
        year = int(quarter_match.group(2))
        ranges = {
            1: ("01-01", "03-31"),
            2: ("04-01", "06-30"),
            3: ("07-01", "09-30"),
            4: ("10-01", "12-31"),
        }
        start, end = ranges[quarter]
        return {
            "label": f"Q{quarter} {year}",
            "start_date": f"{year}-{start}",
            "end_date": f"{year}-{end}",
        }
    return None


def _extract_group_by(query: str) -> str | None:
    patterns = {
        "brand": r"\bbrand\b",
        "category": r"\bcategory\b",
        "region": r"\bregion\b",
        "channel": r"\bchannel\b",
        "promotion_name": r"\bpromotion\b",
        "promotion_type": r"\bcampaign\b|\bpromotion type\b",
    }
    lowered = query.lower()
    for field, pattern in patterns.items():
        if re.search(pattern, lowered):
            return field
    return None


def _extract_metric(query: str) -> str:
    lowered = query.lower()
    if "sales lift" in lowered or "uplift" in lowered:
        return "sales_lift_percent"
    if "spend efficiency" in lowered:
        return "spend_efficiency"
    if "incremental sales" in lowered:
        return "incremental_sales"
    if "trade spend" in lowered:
        return "trade_spend"
    return "roi"


def _extract_intent(query: str, metric: str) -> str:
    lowered = query.lower()
    if any(token in lowered for token in ("should be stopped", "should be reduced", "reduce", "stop")):
        return "recommend_budget_reduction"
    if "high spend" in lowered and any(token in lowered for token in ("weak", "low", "poor")):
        return "find_high_spend_low_performance"
    if any(token in lowered for token in ("highest", "best", "top")):
        if metric == "trade_spend":
            return "find_highest_trade_spend"
        return "find_top_performer"
    if any(token in lowered for token in ("negative", "poor", "low", "weak", "wasted")):
        return "find_low_performing_promotions"
    return "summarize_promotion_performance"


def extract_intent_entities(user_query: str) -> dict:
    query = user_query.strip()
    if not query:
        raise ValueError("user_query cannot be empty.")

    metric = _extract_metric(query)
    filters = {}

    for field, options in (
        ("brand", CATALOG.brands),
        ("category", CATALOG.categories),
        ("region", CATALOG.regions),
        ("channel", CATALOG.channels),
        ("promotion_type", CATALOG.promotion_types),
    ):
        matched = _extract_match(query, options)
        if matched:
            filters[field] = matched

    time_period = _extract_time_period(query)
    if time_period:
        filters["time_period"] = time_period

    dimensions = [
        field for field in ("brand", "category", "region", "channel", "promotion_type") if field in filters
    ]
    group_by = _extract_group_by(query)
    intent = _extract_intent(query, metric)

    return {
        "intent": intent,
        "metric": metric,
        "filters": filters,
        "group_by": group_by,
        "dimensions": dimensions,
    }
