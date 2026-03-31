from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.assistant_engine import build_dashboard_view
from backend.data.mock_data import get_employee_snapshot


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
def get_dashboard(mode: str = "mock"):
    snapshot = get_employee_snapshot(mode=mode)
    return build_dashboard_view(snapshot)
