from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    user_query: str = Field(..., min_length=3, description="Business question in plain English.")


class ExtractedQuery(BaseModel):
    intent: str
    metric: str | None = None
    filters: dict[str, Any] = Field(default_factory=dict)
    group_by: str | None = None
    dimensions: list[str] = Field(default_factory=list)


class ValidationResult(BaseModel):
    is_valid: bool
    sql: str
    reason: str | None = None


class AskResponse(BaseModel):
    user_query: str
    extracted_query: ExtractedQuery
    schema_context: list[dict[str, Any]]
    generated_sql: str
    validation: ValidationResult
    raw_results: list[dict[str, Any]]
    computed_metrics: list[dict[str, Any]]
    answer: str
    recommendation: str | None = None
