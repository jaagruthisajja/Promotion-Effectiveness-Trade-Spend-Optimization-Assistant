from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.services.assistant_engine import build_dashboard_view, normalize_graph_snapshot
from backend.data.mock_data import get_employee_snapshot
from backend.services.graph_client import (
    GraphApiError,
    GraphAuthError,
    fetch_graph_snapshot,
)


app = FastAPI(
    title="Workday Copilot Hub API",
    version="0.1.0",
    description=(
        "Python backend for an employee assistant dashboard that can be wired "
        "to Microsoft 365, Teams, Outlook, and Copilot-style orchestration."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/dashboard")
async def get_dashboard(mode: str = "mock", authorization: str | None = Header(default=None)):
    if mode == "graph":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="A Microsoft Graph access token is required for graph mode.",
            )

        access_token = authorization.removeprefix("Bearer ").strip()

        try:
            graph_snapshot = await fetch_graph_snapshot(access_token)
            snapshot = normalize_graph_snapshot(graph_snapshot)
            return build_dashboard_view(snapshot)
        except GraphAuthError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        except GraphApiError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    snapshot = get_employee_snapshot(mode=mode)
    return build_dashboard_view(snapshot)
