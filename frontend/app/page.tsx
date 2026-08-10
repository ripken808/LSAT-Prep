"use client";

import { useEffect, useState } from "react";
import {
  GradeResult,
  GradeResultView,
  Question,
  QuestionCard,
} from "./_components/QuestionCard";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [question, setQuestion] = useState<Question | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<GradeResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCurrentQuestion();
  }, []);

  async function loadCurrentQuestion() {
    setLoading(true);
    setError(null);
    setResult(null);
    setSelected(null);
    try {
      const res = await fetch(`${API_URL}/api/question/current`);
      if (!res.ok) {
        throw new Error(
          res.status === 404
            ? "No question has been generated yet. Run the generation script first."
            : `Failed to load question (${res.status})`
        );
      }
      setQuestion(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    if (!question || !selected) return;
    setError(null);
    try {
      const res = await fetch(
        `${API_URL}/api/question/${question.id}/grade`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ selected_answer: selected }),
        }
      );
      if (!res.ok) throw new Error(`Grading failed (${res.status})`);
      setResult(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  return (
    <main style={{ maxWidth: 700, margin: "40px auto", padding: "0 16px 60px" }}>
      <h1 style={{ marginBottom: 20 }}>LSAT Prep</h1>

      {loading && <p>Loading question...</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {question && (
        <div>
          <p style={{ fontSize: 12, color: "var(--text-muted)", marginBottom: 10 }}>
            Type: {question.question_type}
          </p>

          {/* Long-form reading content (stimulus, stem, choices) stays in a
              clean, high-contrast, plain-font card - deliberately not
              themed, per the reading-legibility requirement. */}
          <QuestionCard
            question={question}
            selected={selected}
            onSelect={setSelected}
            locked={!!result}
          />

          {!result && (
            <button
              className="block-btn block-btn-primary"
              style={{ marginTop: 20 }}
              onClick={submitAnswer}
              disabled={!selected}
            >
              Submit
            </button>
          )}

          {result && (
            <div style={{ marginTop: 20 }}>
              <GradeResultView result={result} />

              <button className="block-btn block-btn-secondary" onClick={loadCurrentQuestion}>
                Reload
              </button>
            </div>
          )}
        </div>
      )}
    </main>
  );
}
