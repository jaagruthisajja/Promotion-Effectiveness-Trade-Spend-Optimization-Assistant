import { useEffect, useState } from "react";
import { InteractionRequiredAuthError } from "@azure/msal-browser";
import { useIsAuthenticated, useMsal } from "@azure/msal-react";
import { isMsalConfigured, loginRequest } from "./authConfig";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

function ListItem({ kicker, title, meta, chips = [], emphasize = false }) {
  return (
    <article className="list-item">
      <div className="list-item-header">
        <span className="item-kicker">{kicker}</span>
        <span className="muted">{emphasize ? "Action now" : ""}</span>
      </div>
      <h4>{title}</h4>
      <p className="list-meta">{meta}</p>
      <div className="chip-row">
        {chips.map((chip) => (
          <span key={`${title}-${chip.label}`} className={`chip ${chip.tone}`}>
            {chip.label}
          </span>
        ))}
      </div>
    </article>
  );
}

function WorkdayItem({ task }) {
  return (
    <article className="workday-item">
      <div className="workday-header">
        <div>
          <p className="item-kicker">{task.source}</p>
          <h4>{task.title}</h4>
        </div>
        <strong>{task.percentComplete}%</strong>
      </div>
      <p className="list-meta">
        Due {task.displayDueAt} | Priority {task.priority}
      </p>
      <div className="progress">
        <span style={{ width: `${task.percentComplete}%` }} />
      </div>
    </article>
  );
}

function DashboardShell({
  dashboard,
  mode,
  setMode,
  authReady,
  accountName,
  onSignIn,
  onSignOut,
}) {
  return (
    <div className="shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Personal Assistant</p>
          <h1>Workday Copilot Hub</h1>
          <p className="sidebar-copy">
            One place for Teams chats, Outlook mails, meetings, reminders, and
            the employee work plan for the day.
          </p>
        </div>

        <div className="integration-card">
          <p className="section-label">Integration Mode</p>
          <div className="mode-row">
            <span className="badge badge-live">
              {dashboard.integrationMode === "mock" ? "Mock Data" : "Graph Live"}
            </span>
            <select
              className="mode-select"
              value={mode}
              onChange={(event) => setMode(event.target.value)}
            >
              <option value="mock">Mock</option>
              <option value="graph">Graph</option>
            </select>
          </div>
          <p className="integration-copy">{dashboard.integrationCopy}</p>
          {authReady ? (
            <div className="auth-card">
              <span className="auth-label">
                {accountName ? `Signed in as ${accountName}` : "Microsoft 365 not connected"}
              </span>
              {accountName ? (
                <button className="auth-button" onClick={onSignOut} type="button">
                  Sign out
                </button>
              ) : (
                <button className="auth-button" onClick={onSignIn} type="button">
                  Connect Microsoft 365
                </button>
              )}
            </div>
          ) : (
            <p className="integration-copy">
              Add `frontend/.env` values to enable real Microsoft 365 sign-in.
            </p>
          )}
        </div>

        <div className="assistant-card">
          <p className="section-label">Assistant Focus</p>
          <ul className="focus-list">
            {dashboard.focus.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </div>
      </aside>

      <main className="main-content">
        <section className="hero">
          <div>
            <p className="eyebrow">Employee Day View</p>
            <h2>{dashboard.headline}</h2>
            <p className="hero-copy">{dashboard.subheadline}</p>
          </div>

          <div className="hero-stats">
            <div className="stat-card">
              <span className="stat-label">Pending Tasks</span>
              <strong>{dashboard.pendingCount}</strong>
            </div>
            <div className="stat-card">
              <span className="stat-label">Meetings Today</span>
              <strong>{dashboard.meetingCount}</strong>
            </div>
            <div className="stat-card">
              <span className="stat-label">Needs Attention</span>
              <strong>{dashboard.alertCount}</strong>
            </div>
          </div>
        </section>

        <section className="grid">
          <article className="panel panel-wide">
            <div className="panel-header">
              <div>
                <p className="section-label">Next Best Actions</p>
                <h3>Priority Queue</h3>
              </div>
              <span className="panel-pill">Auto-curated</span>
            </div>
            <div className="list-stack">
              {dashboard.priorityQueue.map((item) => (
                <ListItem
                  key={item.id}
                  kicker={item.kind}
                  title={item.title}
                  meta={item.detail}
                  emphasize={item.urgency === "high"}
                  chips={[
                    {
                      label: item.urgency,
                      tone: item.urgency === "high" ? "chip-warn" : "chip-accent",
                    },
                  ]}
                />
              ))}
            </div>
          </article>

          <article className="panel">
            <div className="panel-header">
              <div>
                <p className="section-label">Calendar</p>
                <h3>Meetings to Attend</h3>
              </div>
            </div>
            <div className="list-stack">
              {dashboard.meetingsToday.map((meeting) => (
                <ListItem
                  key={meeting.id}
                  kicker={meeting.mustAttend ? "Required" : "Optional"}
                  title={meeting.title}
                  meta={meeting.displayTime}
                  chips={[
                    { label: meeting.organizer, tone: "chip-info" },
                    { label: meeting.prepNote, tone: "chip-accent" },
                  ]}
                />
              ))}
            </div>
          </article>

          <article className="panel">
            <div className="panel-header">
              <div>
                <p className="section-label">Reminders</p>
                <h3>Upcoming Nudges</h3>
              </div>
            </div>
            <div className="list-stack">
              {dashboard.reminders.map((reminder) => (
                <ListItem
                  key={reminder.id}
                  kicker={reminder.type}
                  title={reminder.title}
                  meta={reminder.displayAt}
                  chips={[
                    {
                      label: "Reminder",
                      tone: reminder.type === "meeting" ? "chip-info" : "chip-warn",
                    },
                  ]}
                />
              ))}
            </div>
          </article>

          <article className="panel">
            <div className="panel-header">
              <div>
                <p className="section-label">Outlook + Teams</p>
                <h3>Inbox and Conversations</h3>
              </div>
            </div>
            <div className="list-stack">
              {dashboard.attentionSignals.map((signal) => (
                <ListItem
                  key={signal.id}
                  kicker={signal.source}
                  title={signal.subject}
                  meta={`${signal.sender} | ${signal.displayReceivedAt}`}
                  chips={[
                    {
                      label: signal.importance,
                      tone: signal.importance === "high" ? "chip-warn" : "chip-accent",
                    },
                    {
                      label: signal.needsReply ? "Reply needed" : "FYI",
                      tone: "chip-info",
                    },
                    {
                      label: signal.extractedTask,
                      tone: "chip-accent",
                    },
                  ]}
                />
              ))}
            </div>
          </article>

          <article className="panel panel-wide">
            <div className="panel-header">
              <div>
                <p className="section-label">Daily Execution</p>
                <h3>Today's Work List</h3>
              </div>
            </div>
            <div className="workday-list">
              {dashboard.workdayList.map((task) => (
                <WorkdayItem key={task.id} task={task} />
              ))}
            </div>
          </article>

          <article className="panel panel-wide">
            <div className="panel-header">
              <div>
                <p className="section-label">Architecture</p>
                <h3>M365 and Copilot Path</h3>
              </div>
            </div>
            <div className="architecture">
              <div>
                <h4>Primary sources</h4>
                <p>
                  Microsoft Graph for Outlook mail, calendar events, Teams
                  conversations, and Microsoft To Do or Planner tasks.
                </p>
              </div>
              <div>
                <h4>Assistant layer</h4>
                <p>
                  Copilot or a custom assistant can summarize threads, extract
                  action items, and convert conversations into reminders.
                </p>
              </div>
              <div>
                <h4>Backend role</h4>
                <p>
                  The Python service is the place to add Graph authentication,
                  Copilot orchestration, prioritization rules, and persistence.
                </p>
              </div>
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}

function StandaloneApp() {
  return <ConnectedApp authEnabled={false} />;
}

function MsalApp() {
  const { instance, accounts } = useMsal();
  const isAuthenticated = useIsAuthenticated();

  async function getGraphToken() {
    const account = accounts[0];
    if (!account) {
      return null;
    }

    try {
      const response = await instance.acquireTokenSilent({
        ...loginRequest,
        account,
      });
      return response.accessToken;
    } catch (error) {
      if (error instanceof InteractionRequiredAuthError) {
        const response = await instance.acquireTokenPopup(loginRequest);
        return response.accessToken;
      }
      throw error;
    }
  }

  async function signIn() {
    await instance.loginPopup(loginRequest);
  }

  async function signOut() {
    const account = accounts[0];
    if (account) {
      await instance.logoutPopup({ account });
    }
  }

  return (
    <ConnectedApp
      authEnabled
      accountName={isAuthenticated ? accounts[0]?.username : ""}
      isAuthenticated={isAuthenticated}
      onSignIn={signIn}
      onSignOut={signOut}
      getGraphToken={getGraphToken}
    />
  );
}

function ConnectedApp({
  authEnabled,
  accountName = "",
  isAuthenticated = false,
  onSignIn = async () => {},
  onSignOut = async () => {},
  getGraphToken = async () => null,
}) {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mode, setMode] = useState("mock");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const headers = {};
        if (mode === "graph") {
          if (!authEnabled) {
            throw new Error("Microsoft sign-in is not configured in the frontend.");
          }
          if (!isAuthenticated) {
            throw new Error("Sign in to Microsoft 365 to load live Outlook, Teams, and To Do data.");
          }

          const token = await getGraphToken();
          if (!token) {
            throw new Error("Unable to acquire a Microsoft Graph access token.");
          }

          headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE}/dashboard?mode=${mode}`, {
          headers,
        });

        if (!response.ok) {
          const errorBody = await response.json().catch(() => ({}));
          throw new Error(errorBody.detail || `Dashboard request failed with ${response.status}`);
        }

        const data = await response.json();
        setDashboard(data);
      } catch (loadError) {
        setError(loadError.message);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [authEnabled, getGraphToken, isAuthenticated, mode]);

  if (loading) {
    return <main className="loading-state">Loading Workday Copilot Hub...</main>;
  }

  if (error && !dashboard) {
    return (
      <main className="loading-state">
        Unable to load the dashboard.
        <br />
        {error}
      </main>
    );
  }

  return (
    <>
      {error ? <div className="top-error-banner">{error}</div> : null}
      <DashboardShell
        dashboard={dashboard}
        mode={mode}
        setMode={setMode}
        authReady={authEnabled}
        accountName={accountName}
        onSignIn={onSignIn}
        onSignOut={onSignOut}
      />
    </>
  );
}

export default function App() {
  return isMsalConfigured() ? <MsalApp /> : <StandaloneApp />;
}
