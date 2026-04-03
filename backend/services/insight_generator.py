from __future__ import annotations


def _format_percent(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.0f}%"


def _format_number(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):,.2f}"


def build_recommendation(top_row: dict | None) -> str | None:
    if not top_row:
        return None

    roi = top_row.get("roi")
    sales_lift = top_row.get("sales_lift_percent")

    if roi is not None and roi < 0:
        return "Recommendation: reduce or redesign this promotion because the spend is not returning value."
    if sales_lift is not None and sales_lift < 20:
        return "Recommendation: review this campaign because the sales lift is too weak for the current spend."
    if roi is not None and roi > 0.5:
        return "Recommendation: consider scaling this campaign or repeating it in similar markets."
    return "Recommendation: keep monitoring performance before reallocating budget."


def generate_insight(user_query: str, rows: list[dict]) -> str:
    if not rows:
        return (
            "No matching promotion data was found for that question. Try changing the region, "
            "channel, promotion type, or time period."
        )

    top_row = rows[0]
    if "promotion_name" in top_row:
        return (
            f"For '{user_query}', the top matching promotion is {top_row['promotion_name']} "
            f"for {top_row.get('brand', 'the selected brand')} in {top_row.get('region', 'the selected region')}. "
            f"It delivered ROI of {_format_percent(top_row.get('roi'))}, sales lift of "
            f"{_format_number(top_row.get('sales_lift_percent'))}%, incremental sales of "
            f"{_format_number(top_row.get('incremental_sales'))}, and trade spend of "
            f"{_format_number(top_row.get('trade_spend'))}."
        )

    dimension = next((key for key in ("brand", "category", "region", "channel", "promotion_type") if key in top_row), "segment")
    return (
        f"For '{user_query}', the strongest matching {dimension} is {top_row[dimension]} "
        f"with an average metric value of {_format_number(top_row.get('metric_value'))} and "
        f"incremental sales of {_format_number(top_row.get('incremental_sales'))}."
    )
