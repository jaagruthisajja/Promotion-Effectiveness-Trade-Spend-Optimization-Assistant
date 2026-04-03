import { useEffect, useState } from "react";

const DEFAULT_API_BASE = "https://promotion-effectiveness-trade-spend-udnh.onrender.com/api";
const API_BASE = (import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE).replace(/\/+$/, "");

const SAMPLE_QUESTIONS = [
  "Which promotion had the highest ROI in South India in Q1 2025?",
  "Show low-performing discount campaigns in Modern Trade.",
  "Which brand got the highest sales lift from promotions in South India?",
  "Which promotions should be reduced based on low ROI?",
];

function StatCard({ label, value, tone = "default" }) {
  return (
    <article className={`stat-card stat-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function KeyValueList({ title, data }) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <p className="eyebrow">Workflow Output</p>
        <h3>{title}</h3>
      </div>
      <div className="kv-list">
        {Object.entries(data || {}).map(([key, value]) => (
          <div className="kv-item" key={key}>
            <span>{key.replaceAll("_", " ")}</span>
            <strong>{typeof value === "object" ? JSON.stringify(value) : String(value)}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function DataTable({ rows }) {
  if (!rows?.length) {
    return <p className="empty-state">No rows returned for this question.</p>;
  }

  const columns = Object.keys(rows[0]);
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column.replaceAll("_", " ")}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.promotion_id || row.brand || "row"}-${index}`}>
              {columns.map((column) => (
                <td key={column}>{String(row[column])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function App() {
  const [question, setQuestion] = useState(SAMPLE_QUESTIONS[0]);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion(selectedQuestion) {
    try {
      setLoading(true);
      setError("");

      const apiResponse = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_query: selectedQuestion }),
      });

      const body = await apiResponse.json().catch(() => ({}));
      if (!apiResponse.ok) {
        throw new Error(body.detail || `Request failed with status ${apiResponse.status}`);
      }

      setResponse(body);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    askQuestion(SAMPLE_QUESTIONS[0]);
  }, []);

  const topMetric = response?.computed_metrics?.[0];

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">Promotion Analytics Assistant</p>
          <h1>Promotion Effectiveness and Trade Spend Optimization</h1>
          <p>
            Ask business questions in plain English, inspect the extracted entities,
            review the generated SQL, and get a grounded answer with ROI, sales lift,
            incremental sales, and spend efficiency.
          </p>
        </div>

        <div className="hero-actions">
          <label className="prompt-card">
            <span>Business question</span>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              rows={4}
            />
          </label>
          <button
            className="primary-button"
            onClick={() => askQuestion(question)}
            type="button"
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Ask assistant"}
          </button>
        </div>
      </section>

      <section className="sample-strip">
        {SAMPLE_QUESTIONS.map((sample) => (
          <button
            key={sample}
            className="sample-chip"
            onClick={() => {
              setQuestion(sample);
              askQuestion(sample);
            }}
            type="button"
          >
            {sample}
          </button>
        ))}
      </section>

      {error ? <div className="error-banner">{error}</div> : null}

      <section className="stats-grid">
        <StatCard label="Validation" value={response?.validation?.is_valid ? "Approved" : "Pending"} tone="good" />
        <StatCard label="Top ROI" value={topMetric?.roi ?? "n/a"} />
        <StatCard label="Sales Lift %" value={topMetric?.sales_lift_percent ?? "n/a"} />
        <StatCard label="Spend Efficiency" value={topMetric?.spend_efficiency ?? "n/a"} tone="accent" />
      </section>

      <section className="content-grid">
        <section className="panel answer-panel">
          <div className="panel-heading">
            <p className="eyebrow">Final Answer</p>
            <h2>Business insight</h2>
          </div>
          <p className="answer-text">{response?.answer || "Submit a question to analyze promotion data."}</p>
          {response?.recommendation ? (
            <div className="recommendation-card">{response.recommendation}</div>
          ) : null}
        </section>

        <KeyValueList title="Extracted intent and entities" data={response?.extracted_query} />

        <section className="panel">
          <div className="panel-heading">
            <p className="eyebrow">SQL Pipeline</p>
            <h3>Generated SQL</h3>
          </div>
          <pre className="sql-block">{response?.generated_sql || "-- waiting for query --"}</pre>
        </section>

        <section className="panel">
          <div className="panel-heading">
            <p className="eyebrow">Schema context</p>
            <h3>Relevant tables</h3>
          </div>
          <div className="schema-list">
            {(response?.schema_context || []).map((table) => (
              <article className="schema-card" key={table.table}>
                <strong>{table.table}</strong>
                <p>{table.description}</p>
                <span>{table.columns.join(", ")}</span>
              </article>
            ))}
          </div>
        </section>

        <section className="panel panel-wide">
          <div className="panel-heading">
            <p className="eyebrow">Computed metrics</p>
            <h3>Promotion results</h3>
          </div>
          <DataTable rows={response?.computed_metrics || []} />
        </section>
      </section>
    </main>
  );
}
