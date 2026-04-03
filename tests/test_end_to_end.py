from fastapi.testclient import TestClient

from backend.main import app


def test_ask_endpoint_returns_business_answer():
    client = TestClient(app)
    response = client.post(
        "/api/ask",
        json={"user_query": "Which promotion had the highest ROI in South India in Q1 2025?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["validation"]["is_valid"] is True
    assert body["raw_results"]
    assert "Summer Saver" in body["answer"]
