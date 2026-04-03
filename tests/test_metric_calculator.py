from backend.services.metric_calculator import calculate_metrics


def test_metric_calculator_handles_zero_trade_spend():
    rows = [
        {
            "promotion_name": "Zero Spend Trial",
            "baseline_sales": 100.0,
            "promoted_sales": 120.0,
            "incremental_sales": 20.0,
            "trade_spend": 0.0,
            "roi": None,
            "sales_lift_percent": None,
            "spend_efficiency": None,
        }
    ]

    result = calculate_metrics(rows)[0]

    assert result["roi"] is None
    assert result["sales_lift_percent"] == 20.0
    assert result["spend_efficiency"] is None
