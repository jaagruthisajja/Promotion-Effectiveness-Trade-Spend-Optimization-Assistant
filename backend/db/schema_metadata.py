SCHEMA_METADATA = {
    "products": {
        "description": "Product hierarchy with brand and category details.",
        "columns": [
            "product_id",
            "product_name",
            "brand",
            "category",
            "subcategory",
        ],
    },
    "regions": {
        "description": "Geography mapping for region, zone, and country.",
        "columns": ["region_id", "region_name", "zone_name", "country"],
    },
    "channels": {
        "description": "Sales channels such as Modern Trade and E-commerce.",
        "columns": ["channel_id", "channel_name"],
    },
    "promotions": {
        "description": "Promotion campaigns with spend and campaign dates.",
        "columns": [
            "promotion_id",
            "promotion_name",
            "promotion_type",
            "start_date",
            "end_date",
            "product_id",
            "region_id",
            "channel_id",
            "trade_spend",
        ],
    },
    "promotion_performance": {
        "description": "Calculated promotion metrics such as ROI and sales lift.",
        "columns": [
            "promotion_id",
            "baseline_sales",
            "promoted_sales",
            "incremental_sales",
            "roi",
            "sales_lift_percent",
        ],
    },
    "sales": {
        "description": "Observed sales measures by product, region, channel, and date.",
        "columns": [
            "sales_id",
            "product_id",
            "region_id",
            "channel_id",
            "date",
            "units_sold",
            "revenue",
        ],
    },
}

METRIC_FORMULAS = {
    "roi": "(promotion_performance.incremental_sales - promotions.trade_spend) / promotions.trade_spend",
    "sales_lift_percent": (
        "((promotion_performance.promoted_sales - promotion_performance.baseline_sales) "
        "/ promotion_performance.baseline_sales) * 100"
    ),
    "spend_efficiency": "promotion_performance.incremental_sales / promotions.trade_spend",
}

APPROVED_TABLES = set(SCHEMA_METADATA.keys())
