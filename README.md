# Promotion Effectiveness & Trade Spend Optimization Assistant

This project is a FastAPI + React application that turns plain-English promotion questions into safe SQL-backed business answers.

## What the app does

- accepts a promotion analytics question in plain English
- extracts intent, metric, filters, and dimensions
- retrieves relevant schema context
- generates a safe SQL `SELECT` query
- validates the SQL against a whitelist
- executes the query on a seeded local SQLite database
- returns a business-friendly answer plus raw results and computed metrics

## Stack

- Backend: FastAPI
- Frontend: React with Vite
- Local database: SQLite seeded from SQL scripts
- Testing: pytest

## Project structure

- `backend/main.py`: FastAPI entry point
- `backend/api/routes.py`: `/api/health` and `/api/ask`
- `backend/services/`: extractor, schema retrieval, SQL generation, validation, execution, metrics, insight pipeline
- `backend/db/schema.sql`: local database schema
- `backend/db/sample_data.sql`: seeded promotion records
- `frontend/src/App.jsx`: promotion analytics UI
- `tests/`: unit and end-to-end coverage

## Run the backend

```powershell
cd C:\Users\jaagruthi.sajja\Documents\Playground
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## Run the frontend

```powershell
cd C:\Users\jaagruthi.sajja\Documents\Playground\frontend
npm install
npm run dev
```

The frontend runs at `http://127.0.0.1:5173`.

Set `VITE_API_BASE_URL` in `frontend/.env` if you want to point the UI at a different API base URL.

## API endpoints

- `GET /api/health`
- `POST /api/ask`

Example request:

```json
{
  "user_query": "Which promotion had the highest ROI in South India in Q1 2025?"
}
```

## Sample questions

- Which promotion had the highest ROI in South India in Q1 2025?
- Which brand got the highest sales lift from promotions in South India?
- Show low-performing discount campaigns in Modern Trade.
- Which region had high trade spend but weak uplift?
- Which promotions should be reduced based on low ROI?

## Run tests

```powershell
cd C:\Users\jaagruthi.sajja\Documents\Playground
pytest
```

## Notes

- The framework asked for MySQL as a production-oriented executor; this MVP uses a seeded local SQLite database so the app runs immediately in this workspace.
- Database path defaults to `backend/db/promotion_optimization.db`.
- Override the database location with `PROMOTION_DB_PATH` if needed.
