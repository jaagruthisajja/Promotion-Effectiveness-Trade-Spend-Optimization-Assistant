from __future__ import annotations

from backend.db.connection import initialize_database
from backend.db.schema_metadata import METRIC_FORMULAS
from backend.models.request_response import AskResponse, ExtractedQuery, ValidationResult
from backend.services.db_executor import execute_query
from backend.services.insight_generator import build_recommendation, generate_insight
from backend.services.intent_extractor import extract_intent_entities
from backend.services.metric_calculator import calculate_metrics
from backend.services.schema_retriever import retrieve_schema_context
from backend.services.sql_generator import generate_sql
from backend.services.sql_validator import validate_sql


def run_pipeline(user_query: str) -> AskResponse:
    initialize_database()
    extracted = extract_intent_entities(user_query)
    schema_context = retrieve_schema_context(extracted)
    generated_sql = generate_sql(user_query, extracted, schema_context, METRIC_FORMULAS)
    validation = validate_sql(generated_sql)

    if not validation["is_valid"]:
        return AskResponse(
            user_query=user_query,
            extracted_query=ExtractedQuery(**extracted),
            schema_context=schema_context,
            generated_sql=generated_sql,
            validation=ValidationResult(**validation),
            raw_results=[],
            computed_metrics=[],
            answer=validation["reason"] or "The generated SQL was rejected.",
            recommendation=None,
        )

    raw_results = execute_query(validation["sql"])
    computed_metrics = calculate_metrics(raw_results)
    answer = generate_insight(user_query, computed_metrics)
    recommendation = build_recommendation(computed_metrics[0] if computed_metrics else None)

    return AskResponse(
        user_query=user_query,
        extracted_query=ExtractedQuery(**extracted),
        schema_context=schema_context,
        generated_sql=validation["sql"],
        validation=ValidationResult(**validation),
        raw_results=raw_results,
        computed_metrics=computed_metrics,
        answer=answer,
        recommendation=recommendation,
    )
