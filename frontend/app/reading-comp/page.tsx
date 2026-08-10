"use client";

import { useEffect, useState } from "react";
import {
  GradeResult,
  GradeResultView,
  Question,
  QuestionCard,
  formatQuestionType,
} from "../_components/QuestionCard";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Passage = {
  id: number;
  content_area: string;
  title: string | null;
  passage_text: string;
};

type PassageWithQuestions = {
  passage: Passage;
  questions: Question[];
};

export default function ReadingCompPage() {
  const [data, setData] = useState<PassageWithQuestions | null>(null);
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<GradeResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadNewPassage();
  }, []);

  async function loadNewPassage() {
    setLoading(true);
    setError(null);
    setResult(null);
    setSelected(null);
    setIndex(0);
    try {
      const res = await fetch(`${API_URL}/api/passage/random`);
      if (!res.ok) {
        throw new Error(
          res.status === 404
            ? "No passages have been added yet."
            : `Failed to load passage (${res.status})`
        );
      }
      setData(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  function nextQuestion() {
    setResult(null);
    setSelected(null);
    setIndex((i) => i + 1);
  }

  async function submitAnswer() {
    const question = data?.questions[index];
    if (!question || !selected) return;
    setError(null);
    try {
      const res = await fetch(`${API_URL}/api/question/${question.id}/grade`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ selected_answer: selected }),
      });
      if (!res.ok) throw new Error(`Grading failed (${res.status})`);
      setResult(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  const question = data?.questions[index];
  const isLastQuestion = data ? index >= data.questions.length - 1 : false;

  return (
    <main style={{ maxWidth: 800, margin: "40px auto", padding: "0 16px 60px" }}>
      <h1 style={{ marginBottom: 20 }}>Reading Comprehension</h1>

      {loading && <p>Loading passage...</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {data && question && (
        <div style={{ display: "flex", gap: 24, alignItems: "flex-start", flexWrap: "wrap" }}>
          {/* Passage stays pinned/visible while cycling through its questions -
              same clean-card treatment as LR stimulus/explanation: plain,
              high-contrast, untouched by the pixel theme. */}
          <div className="clean-card" style={{ flex: "1 1 380px", maxHeight: 640, overflowY: "auto" }}>
            <p style={{ fontSize: 12, color: "#666", marginBottom: 10 }}>
              {data.passage.content_area.replace("_", " ")}
            </p>
            {data.passage.title && (
              <p style={{ marginBottom: 12 }}><strong>{data.passage.title}</strong></p>
            )}
            {data.passage.passage_text.split("\n\n").map((para, i) => (
              <p key={i} style={{ marginBottom: 12 }}>{para}</p>
            ))}
          </div>

          <div style={{ flex: "1 1 340px" }}>
            <p style={{ fontSize: 12, color: "var(--text-muted)", marginBottom: 10 }}>
              Question {index + 1} of {data.questions.length} &middot; Type: {formatQuestionType(question.question_type)}
            </p>

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

                {isLastQuestion ? (
                  <button className="block-btn block-btn-secondary" onClick={loadNewPassage}>
                    New Passage
                  </button>
                ) : (
                  <button className="block-btn block-btn-primary" onClick={nextQuestion}>
                    Next Question
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </main>
  );
}
