from backend.services.sql_validator import validate_sql


def test_validator_accepts_select_and_adds_limit():
    result = validate_sql("SELECT * FROM promotions")

    assert result["is_valid"] is True
    assert "LIMIT 100" in result["sql"]


def test_validator_rejects_delete_statement():
    result = validate_sql("DELETE FROM promotions")

    assert result["is_valid"] is False
    assert result["reason"] == "Only SELECT queries are allowed."
