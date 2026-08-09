"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Question = {
  id: number;
  section: string;
  question_type: string;
  content_area: string | null;
  stimulus: string;
  question_stem: string;
  choices: string[];
};

type GradeResult = {
  correct: boolean;
  correct_answer: string;
  explanation: string;
};

const LETTERS = ["A", "B", "C", "D", "E"];

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
          <div className="clean-card">
            <p style={{ marginBottom: 16 }}>{question.stimulus}</p>
            <p style={{ marginBottom: 16 }}><strong>{question.question_stem}</strong></p>

            <form>
              {question.choices.map((choice, i) => (
                <label key={i} style={{ display: "block", margin: "10px 0" }}>
                  <input
                    type="radio"
                    name="choice"
                    value={LETTERS[i]}
                    checked={selected === LETTERS[i]}
                    onChange={() => setSelected(LETTERS[i])}
                    disabled={!!result}
                  />
                  {" "}({LETTERS[i]}) {choice}
                </label>
              ))}
            </form>
          </div>

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
              <div
                className={`result-chip ${result.correct ? "result-chip-correct" : "result-chip-incorrect"}`}
              >
                {result.correct ? "Correct!" : "Incorrect."} Correct answer: {result.correct_answer}
              </div>

              <div className="clean-card" style={{ marginBottom: 16 }}>
                <p>{result.explanation}</p>
              </div>

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
