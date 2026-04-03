# Deployment Guide

This document explains how to deploy the Promotion Effectiveness & Trade Spend Optimization project.

The project has two deployable parts:

- `backend/` = FastAPI API
- `frontend/` = React app built with Vite

## 1. Current architecture

This project does not require Groq, Railway, or MySQL for the current MVP.

The backend uses:

- FastAPI
- a local SQLite database created automatically from:
  - `backend/db/schema.sql`
  - `backend/db/sample_data.sql`

The frontend uses:

- React
- Vite

Important deployment note:

- the SQLite database is file-based
- that is fine for demo or MVP deployment
- on many cloud platforms, container filesystem storage is ephemeral
- if the backend restarts, the database file may be recreated from the seed SQL

That means the deployed app is best treated as a seeded demo unless you later move to a persistent external database.

## 2. Recommended deployment setup

Use this setup:

- Render Web Service for the backend
- Render Static Site for the frontend

## 3. Deploy the backend on Render

### 3.1 Create the backend service

1. Log in to Render.
2. Click `New +`.
3. Click `Web Service`.
4. Connect the GitHub repo for this project.

### 3.2 Use these Render backend settings

- Name: `promotion-effectiveness-trade-spend-backend` or any name you want
- Branch: `main`
- Root Directory: `backend`
- Environment: `Docker`
- Dockerfile Path: `Dockerfile`
- Region: choose the closest region to your users
- Instance Type: `Starter` is enough for MVP

### 3.3 Backend environment variables

No required secret environment variables are needed for the current seeded SQLite MVP.

Optional:

- `PROMOTION_DB_PATH`

Recommended value:

```text
PROMOTION_DB_PATH=/app/backend/db/promotion_optimization.db
```

If you do not set it, the app will still use the default path inside the container.

### 3.4 Backend health check

Set:

- Health Check Path: `/api/health`

### 3.5 Deploy and test the backend

1. Click `Create Web Service`.
2. Wait for Render to finish deployment.
3. Open the backend URL and test:

```text
https://your-backend-service.onrender.com/api/health
```

Expected response:

```json
{"status":"ok"}
```

Also test the main API:

```text
POST https://your-backend-service.onrender.com/api/ask
```

Example JSON body:

```json
{
  "user_query": "Which promotion had the highest ROI in South India in Q1 2025?"
}
```

### 3.6 Current deployed backend

The current frontend default points to:

[https://promotion-effectiveness-trade-spend-udnh.onrender.com/api](https://promotion-effectiveness-trade-spend-udnh.onrender.com/api)

## 4. Deploy the frontend on Render

### 4.1 Create the frontend service

1. In Render, click `New +`.
2. Click `Static Site`.
3. Select the same GitHub repo.

### 4.2 Use these Render frontend settings

- Name: `promotion-effectiveness-trade-spend-frontend` or any name you want
- Branch: `main`
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`

### 4.3 Frontend environment variable

Set:

- `VITE_API_BASE_URL`

Example:

```text
VITE_API_BASE_URL=https://promotion-effectiveness-trade-spend-udnh.onrender.com/api
```

If you do not set it, the frontend already falls back to this deployed backend URL in code.

Still, setting it in Render is recommended so the deployed frontend configuration is explicit.

### 4.4 Deploy the frontend

1. Click `Create Static Site`.
2. Wait for deployment to complete.
3. Open the frontend Render URL in your browser.
4. Ask a sample question and confirm the UI shows:
   - extracted entities
   - generated SQL
   - final answer
   - result table

## 5. How frontend and backend connect

The frontend calls:

- `VITE_API_BASE_URL + /ask`

In code this is handled in:

- `frontend/src/App.jsx`

The backend exposes:

- `GET /api/health`
- `POST /api/ask`

The backend initializes the SQLite database automatically from:

- `backend/db/schema.sql`
- `backend/db/sample_data.sql`

## 6. Local build and test before deployment

### Backend

From the repo root:

```powershell
.venv\Scripts\activate
.venv\Scripts\python -m pytest
uvicorn backend.main:app --reload
```

### Frontend

From `frontend/`:

```powershell
npm install
npm run build
npm run dev
```

## 7. Docker deployment notes for the backend

The backend Dockerfile is in:

- `backend/Dockerfile`

It is currently written for a deployment flow where the Render root directory is `backend`.

That is why the Dockerfile uses paths like:

```dockerfile
COPY requirements.txt ./backend/requirements.txt
COPY . ./backend
```

Those paths are correct when Render builds with:

- Root Directory: `backend`

If you change the Render root directory later, you may also need to update the Dockerfile copy paths.

## 8. How to update the application later

1. Make code changes locally.
2. Commit the changes.
3. Push to GitHub.

If Render auto deploy is enabled:

- frontend and backend redeploy automatically

If auto deploy is not enabled:

1. Open the Render service
2. Click `Manual Deploy`
3. Click `Deploy latest commit`

## 9. Common deployment problems and fixes

### Problem: backend Docker build fails with `requirements.txt not found`

Cause:

- Render root directory and Dockerfile copy paths do not match

Fix:

- if Root Directory is `backend`, keep:

```dockerfile
COPY requirements.txt ./backend/requirements.txt
COPY . ./backend
```

### Problem: frontend loads but API requests fail

Cause:

- wrong backend URL
- missing `VITE_API_BASE_URL`
- CORS issue

Fix:

- set `VITE_API_BASE_URL` to the correct backend Render URL
- confirm backend is reachable at `/api/health`
- verify backend CORS allows requests

### Problem: backend works locally but deployed data resets

Cause:

- SQLite database file is stored inside the container filesystem

Fix:

- expected for demo-style deployments
- move to a persistent external database for production use

### Problem: backend health check fails

Cause:

- wrong health check path

Fix:

- use `/api/health`

## 10. Deployment checklist

### Backend on Render

- Root Directory = `backend`
- Environment = `Docker`
- Dockerfile Path = `Dockerfile`
- Health Check Path = `/api/health`
- optional `PROMOTION_DB_PATH` set

### Frontend on Render

- Root Directory = `frontend`
- Build Command = `npm install && npm run build`
- Publish Directory = `dist`
- `VITE_API_BASE_URL` set to backend URL

## 11. Recommended deployment order

Use this order:

1. Deploy backend on Render
2. Confirm `/api/health` works
3. Confirm `/api/ask` works
4. Deploy frontend on Render
5. Set `VITE_API_BASE_URL` to backend URL
6. Open frontend and test sample questions
