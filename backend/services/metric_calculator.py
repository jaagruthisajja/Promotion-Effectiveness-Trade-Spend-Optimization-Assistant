from __future__ import annotations


def _safe_ratio(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return round(float(numerator) / float(denominator), 2)


def calculate_metrics(rows: list[dict]) -> list[dict]:
    enriched_rows = []
    for row in rows:
        baseline_sales = row.get("baseline_sales")
        promoted_sales = row.get("promoted_sales")
        incremental_sales = row.get("incremental_sales")
        trade_spend = row.get("trade_spend")

        if row.get("roi") is None:
            roi = _safe_ratio((incremental_sales or 0) - (trade_spend or 0), trade_spend)
        else:
            roi = round(float(row["roi"]), 2)

        if row.get("sales_lift_percent") is None:
            sales_lift = _safe_ratio((promoted_sales or 0) - (baseline_sales or 0), baseline_sales)
            sales_lift = None if sales_lift is None else round(sales_lift * 100, 2)
        else:
            sales_lift = round(float(row["sales_lift_percent"]), 2)

        spend_efficiency = row.get("spend_efficiency")
        if spend_efficiency is None:
            spend_efficiency = _safe_ratio(incremental_sales, trade_spend)
        else:
            spend_efficiency = round(float(spend_efficiency), 2)

        enriched_row = dict(row)
        enriched_row["roi"] = roi
        enriched_row["sales_lift_percent"] = sales_lift
        enriched_row["spend_efficiency"] = spend_efficiency
        enriched_rows.append(enriched_row)

    return enriched_rows
