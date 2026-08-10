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

type TypeCount = { section: string; question_type: string; count: number };
type ContentAreaCount = { content_area: string; count: number };
type Taxonomy = { types: TypeCount[]; content_areas: ContentAreaCount[] };

const SECTION_LABELS: Record<string, string> = {
  logical_reasoning: "Logical Reasoning",
  reading_comprehension: "Reading Comprehension",
};

function formatContentArea(area: string): string {
  return area
    .split("_")
    .map((word) => word[0].toUpperCase() + word.slice(1))
    .join(" ");
}

export default function FocusPage() {
  const [taxonomy, setTaxonomy] = useState<Taxonomy | null>(null);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [selectedAreas, setSelectedAreas] = useState<string[]>([]);

  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<GradeResult | null>(null);
  const [correctCount, setCorrectCount] = useState(0);

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTaxonomy();
  }, []);

  async function loadTaxonomy() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/api/taxonomy`);
      if (!res.ok) throw new Error(`Failed to load filters (${res.status})`);
      setTaxonomy(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  function toggle(list: string[], value: string): string[] {
    return list.includes(value)
      ? list.filter((v) => v !== value)
      : [...list, value];
  }

  async function startSession() {
    setError(null);
    setLoading(true);
    try {
      const params = new URLSearchParams();
      selectedTypes.forEach((t) => params.append("question_type", t));
      selectedAreas.forEach((a) => params.append("content_area", a));

      const res = await fetch(
        `${API_URL}/api/questions/filtered?${params.toString()}`
      );
      if (!res.ok) throw new Error(`Failed to load questions (${res.status})`);

      const body = await res.json();
      setQuestions(body.questions);
      setIndex(0);
      setSelected(null);
      setResult(null);
      setCorrectCount(0);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  function endSession() {
    setQuestions(null);
    setSelected(null);
    setResult(null);
    setIndex(0);
  }

  function nextQuestion() {
    setResult(null);
    setSelected(null);
    setIndex((i) => i + 1);
  }

  async function submitAnswer() {
    const question = questions?.[index];
    if (!question || !selected) return;
    setError(null);
    try {
      const res = await fetch(`${API_URL}/api/question/${question.id}/grade`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ selected_answer: selected }),
      });
      if (!res.ok) throw new Error(`Grading failed (${res.status})`);
      const graded: GradeResult = await res.json();
      setResult(graded);
      if (graded.correct) setCorrectCount((c) => c + 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  const question = questions?.[index];
  const isLastQuestion = questions ? index >= questions.length - 1 : false;
  const sessionFinished =
    questions !== null && questions.length > 0 && index >= questions.length;

  // Group the taxonomy by section so the two sections' types don't run
  // together in one undifferentiated list.
  const typesBySection = (taxonomy?.types ?? []).reduce<
    Record<string, TypeCount[]>
  >((acc, t) => {
    (acc[t.section] ??= []).push(t);
    return acc;
  }, {});

  return (
    <main style={{ maxWidth: 800, margin: "40px auto", padding: "0 16px 60px" }}>
      <h1 style={{ marginBottom: 20 }}>Focus Practice</h1>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {/* Filter picker - shown until a session starts */}
      {taxonomy && questions === null && (
        <div>
          <p style={{ marginBottom: 20, color: "var(--text-secondary)" }}>
            Pick the question types you want to drill. Leave everything
            unselected to practice the whole bank.
          </p>

          {Object.entries(typesBySection).map(([section, types]) => (
            <div key={section} className="wood-panel" style={{ padding: 16, marginBottom: 16 }}>
              <h2 style={{ fontSize: 14, marginBottom: 12 }}>
                {SECTION_LABELS[section] ?? section}
              </h2>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px 20px" }}>
                {types.map((t) => (
                  <label key={t.question_type} style={{ display: "block" }}>
                    <input
                      type="checkbox"
                      checked={selectedTypes.includes(t.question_type)}
                      onChange={() =>
                        setSelectedTypes((prev) => toggle(prev, t.question_type))
                      }
                    />{" "}
                    {formatQuestionType(t.question_type)} ({t.count})
                  </label>
                ))}
              </div>
            </div>
          ))}

          {taxonomy.content_areas.length > 0 && (
            <div className="wood-panel" style={{ padding: 16, marginBottom: 16 }}>
              <h2 style={{ fontSize: 14, marginBottom: 12 }}>Content Area</h2>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px 20px" }}>
                {taxonomy.content_areas.map((a) => (
                  <label key={a.content_area} style={{ display: "block" }}>
                    <input
                      type="checkbox"
                      checked={selectedAreas.includes(a.content_area)}
                      onChange={() =>
                        setSelectedAreas((prev) => toggle(prev, a.content_area))
                      }
                    />{" "}
                    {formatContentArea(a.content_area)} ({a.count})
                  </label>
                ))}
              </div>
            </div>
          )}

          <button
            className="block-btn block-btn-primary"
            style={{ marginTop: 8 }}
            onClick={startSession}
          >
            Start Session
          </button>
          {(selectedTypes.length > 0 || selectedAreas.length > 0) && (
            <button
              className="block-btn block-btn-secondary"
              style={{ marginTop: 8, marginLeft: 10 }}
              onClick={() => {
                setSelectedTypes([]);
                setSelectedAreas([]);
              }}
            >
              Clear
            </button>
          )}
        </div>
      )}

      {/* An empty match is a valid outcome, not an error */}
      {questions !== null && questions.length === 0 && (
        <div>
          <p style={{ marginBottom: 16 }}>
            No questions match those filters.
          </p>
          <button className="block-btn block-btn-secondary" onClick={endSession}>
            Change Filters
          </button>
        </div>
      )}

      {sessionFinished && (
        <div>
          <div className="wood-panel" style={{ padding: 20, marginBottom: 16 }}>
            <h2 style={{ fontSize: 14, marginBottom: 8 }}>Session complete</h2>
            <p>
              {correctCount} of {questions.length} correct
            </p>
          </div>
          <button className="block-btn block-btn-primary" onClick={endSession}>
            New Session
          </button>
        </div>
      )}

      {question && (
        <div>
          <p style={{ fontSize: 12, color: "var(--text-muted)", marginBottom: 10 }}>
            Question {index + 1} of {questions!.length} &middot; Type:{" "}
            {formatQuestionType(question.question_type)}
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
              <button
                className="block-btn block-btn-primary"
                onClick={nextQuestion}
              >
                {isLastQuestion ? "Finish Session" : "Next Question"}
              </button>
            </div>
          )}
        </div>
      )}
    </main>
  );
}
