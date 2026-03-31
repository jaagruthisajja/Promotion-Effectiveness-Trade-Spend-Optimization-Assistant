# Workday Copilot Hub

This project is now structured as a Python + React application for an employee personal assistant dashboard.

## Stack

- Python backend: FastAPI
- JavaScript UI: React with Vite
- Data model: mock Microsoft 365-style data, ready for Graph integration

## Features

- shows Outlook and Teams attention signals
- highlights pending tasks and reminders
- lists must-attend meetings
- surfaces the employee's daily work plan
- keeps a clear path to M365, Graph, and Copilot integration

## Project structure

- `backend/`: Python API
- `frontend/`: React UI
- `requirements.txt`: Python dependencies

The earlier root `index.html` prototype is still present, but the main app going forward is the Python + React stack.

## Run the backend

```powershell
cd C:\Users\jaagruthi.sajja\Documents\Playground
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

## Run the frontend

```powershell
cd C:\Users\jaagruthi.sajja\Documents\Playground\frontend
copy .env.example .env
npm install
npm run dev
```

The React app will run at `http://127.0.0.1:5173`.

## Microsoft 365 app registration

To use live Outlook, Teams, calendar, and To Do data, register an application in Microsoft Entra ID and put its values in `frontend/.env`.

Required frontend env vars:

- `VITE_AZURE_CLIENT_ID`
- `VITE_AZURE_TENANT_ID`
- `VITE_AZURE_REDIRECT_URI`
- `VITE_API_BASE_URL`

Recommended redirect URI for local development:

- `http://127.0.0.1:5173`

Recommended delegated Graph scopes for this app:

- `User.Read`
- `Mail.Read`
- `Calendars.Read`
- `Tasks.Read`
- `Chat.Read`

## API endpoints

- `GET /api/health`
- `GET /api/dashboard?mode=mock`
- `GET /api/dashboard?mode=graph`

`graph` mode now expects a Microsoft Graph bearer token from the React app and loads live Microsoft 365 data through the Python backend.

## Microsoft 365 integration path

For production use, the recommended architecture is:

1. Authenticate users with Microsoft Entra ID.
2. Use Microsoft Graph to read Outlook mail, calendar events, Teams messages, and Microsoft To Do tasks.
3. Use Copilot or a custom assistant layer to summarize conversations, extract tasks, identify required meetings, and generate reminders.
4. Persist user reminders, task status, and preferences in a backend store.

### Suggested Graph endpoints

- `GET /me/messages`
- `GET /me/events`
- `GET /me/todo/lists/{listId}/tasks`
- Microsoft Graph Teams chat, channel message, and online meeting endpoints

### Common delegated permissions

- `User.Read`
- `Mail.Read`
- `Calendars.Read`
- `Tasks.Read`
- `Chat.Read`

Some Teams-related permissions may require admin consent depending on tenant policy and whether you expand beyond personal chats.

## Recommended next step

The next implementation step is to add:

- Copilot or LLM orchestration for task extraction
- richer Teams support for channels and meeting chat
- persistent reminder rules
- task completion and snooze actions
- persistent reminders and task updates
