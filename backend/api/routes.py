from fastapi import APIRouter, HTTPException

from backend.models.request_response import AskRequest, AskResponse
from backend.services.query_pipeline import run_pipeline

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    try:
        return run_pipeline(payload.user_query)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(
            status_code=500,
            detail="The promotion analytics workflow failed to complete.",
        ) from exc
