"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type OverallStats = {
  total: number;
  correct: number;
  accuracy: number | null;
};

type TypeStats = {
  question_type: string;
  total: number;
  correct: number;
  accuracy: number;
};

type DayStats = {
  date: string;
  count: number;
};

type StatsSummary = {
  overall: OverallStats;
  by_type: TypeStats[];
  over_time: DayStats[];
};

function formatQuestionType(type: string): string {
  return type
    .split("_")
    .map((word) => word[0].toUpperCase() + word.slice(1))
    .join(" ");
}

function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export default function ProgressPage() {
  const [stats, setStats] = useState<StatsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_URL}/api/stats/summary`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load stats (${res.status})`);
        return res.json();
      })
      .then(setStats)
      .catch((err) => setError(err instanceof Error ? err.message : String(err)));
  }, []);

  if (error) {
    return (
      <main className="stats-page">
        <h1>Progress</h1>
        <p style={{ color: "crimson" }}>{error}</p>
      </main>
    );
  }

  if (!stats) {
    return (
      <main className="stats-page">
        <h1>Progress</h1>
        <p>Loading...</p>
      </main>
    );
  }

  const { overall, by_type, over_time } = stats;
  const maxDayCount = Math.max(1, ...over_time.map((d) => d.count));

  return (
    <main className="stats-page">
      <h1>Progress</h1>

      <div className="stat-tile">
        <div className="stat-tile-label">Overall accuracy</div>
        <div className="stat-tile-value">
          {overall.accuracy === null ? "—" : formatPercent(overall.accuracy)}
        </div>
        <div className="meter-track">
          <div
            className="meter-fill"
            style={{
              width:
                overall.accuracy === null
                  ? "0%"
                  : `${overall.accuracy * 100}%`,
            }}
          />
        </div>
        <div className="stat-tile-sub">
          {overall.correct} correct out of {overall.total} attempted
        </div>
      </div>

      <section className="stats-section">
        <h2>Accuracy by question type</h2>
        {by_type.length === 0 ? (
          <p className="stats-empty">No attempts yet.</p>
        ) : (
          <table className="bar-table">
            <tbody>
              {by_type.map((row) => (
                <tr key={row.question_type}>
                  <td className="bar-label">{formatQuestionType(row.question_type)}</td>
                  <td className="bar-cell">
                    <div className="bar-track">
                      <div
                        className="bar-fill"
                        style={{ width: `${row.accuracy * 100}%` }}
                      />
                    </div>
                  </td>
                  <td className="bar-value">
                    {formatPercent(row.accuracy)} ({row.correct}/{row.total})
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section className="stats-section">
        <h2>Attempts over time</h2>
        {over_time.length === 0 ? (
          <p className="stats-empty">No attempts yet.</p>
        ) : (
          <table className="bar-table">
            <tbody>
              {over_time.map((row) => (
                <tr key={row.date}>
                  <td className="bar-label">{row.date}</td>
                  <td className="bar-cell">
                    <div className="bar-track">
                      <div
                        className="bar-fill"
                        style={{ width: `${(row.count / maxDayCount) * 100}%` }}
                      />
                    </div>
                  </td>
                  <td className="bar-value">{row.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}
