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
npm install
npm run dev
```

The React app will run at `http://127.0.0.1:5173`.

## API endpoints

- `GET /api/health`
- `GET /api/dashboard?mode=mock`
- `GET /api/dashboard?mode=graph`

`graph` mode currently shows the Graph-ready state while still using placeholder data.

## Microsoft 365 integration path

For production use, the recommended architecture is:

1. Authenticate users with Microsoft Entra ID.
2. Use Microsoft Graph to read Outlook mail, calendar events, Teams messages, and Microsoft To Do or Planner tasks.
3. Use Copilot or a custom assistant layer to summarize conversations, extract tasks, identify required meetings, and generate reminders.
4. Persist user reminders, task status, and preferences in a backend store.

### Suggested Graph endpoints

- `GET /me/messages`
- `GET /me/events`
- `GET /me/todo/lists/{listId}/tasks`
- Microsoft Graph Teams chat, channel message, and online meeting endpoints

### Common delegated permissions

- `Mail.Read`
- `Mail.ReadWrite`
- `Calendars.Read`
- `Tasks.Read`
- `Tasks.ReadWrite`
- `Chat.Read`
- `ChannelMessage.Read.All`
- `OnlineMeetings.Read`

Some Teams permissions may require admin consent.

## Recommended next step

The next implementation step is to add:

- Entra ID sign-in
- Graph token acquisition
- backend Graph connectors
- Copilot or LLM orchestration for task extraction
- persistent reminders and task updates
