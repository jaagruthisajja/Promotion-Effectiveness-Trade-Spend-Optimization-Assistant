from backend.services.intent_extractor import extract_intent_entities


def test_extracts_roi_region_category_and_time_period():
    result = extract_intent_entities(
        "Which promotions had poor ROI in South India for Shampoos in Q1 2025?"
    )

    assert result["intent"] == "find_low_performing_promotions"
    assert result["metric"] == "roi"
    assert result["filters"]["region"] == "South India"
    assert result["filters"]["category"] == "Shampoos"
    assert result["filters"]["time_period"]["label"] == "Q1 2025"
