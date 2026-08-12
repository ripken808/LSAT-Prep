"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  GradeResultView,
  Question,
  QuestionCard,
  formatQuestionType,
} from "../_components/QuestionCard";
import { TimerDisplay, useCountdown } from "../_components/Timer";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Passage = {
  id: number;
  content_area: string;
  title: string | null;
  passage_text: string;
};

type Section = {
  kind: string;
  label: string;
  minutes: number;
  passages: Passage[];
  questions: Question[];
};

type TestPaper = { preset: string; sections: Section[]; warnings: string[] };

type QuestionResult = {
  question_id: number;
  selected_answer: string | null;
  correct: boolean;
  correct_answer: string;
  explanation: string;
};

type GradeResponse = {
  total: number;
  correct: number;
  answered: number;
  results: QuestionResult[];
};

type Phase = "idle" | "running" | "break" | "grading" | "results";

export default function TestPage() {
  const [paper, setPaper] = useState<TestPaper | null>(null);
  const [phase, setPhase] = useState<Phase>("idle");
  const [sectionIndex, setSectionIndex] = useState(0);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [deadline, setDeadline] = useState<number | null>(null);
  const [score, setScore] = useState<GradeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const remaining = useCountdown(phase === "running" ? deadline : null);
  const section = paper?.sections[sectionIndex];
  const isLastSection = paper ? sectionIndex >= paper.sections.length - 1 : false;

  // Build the paper up front so the start screen can state the content gap
  // before the test begins, rather than implying it is full-length.
  const loadPaper = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/api/test/new?preset=reduced`);
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail ?? `Failed to build a test (${res.status})`);
      }
      setPaper(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPaper();
  }, [loadPaper]);

  function startTest() {
    if (!paper) return;
    setAnswers({});
    setSectionIndex(0);
    setQuestionIndex(0);
    setScore(null);
    setDeadline(Date.now() + paper.sections[0].minutes * 60_000);
    setPhase("running");
  }

  async function restartTest() {
    setPhase("idle");
    await loadPaper();
  }

  const submitTest = useCallback(
    async (finalAnswers: Record<number, string>, built: TestPaper) => {
      setPhase("grading");
      setError(null);
      try {
        const payload = built.sections.flatMap((s) =>
          s.questions.map((q) => ({
            question_id: q.id,
            selected_answer: finalAnswers[q.id] ?? null,
          }))
        );
        const res = await fetch(`${API_URL}/api/test/grade`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ answers: payload }),
        });
        if (!res.ok) throw new Error(`Grading failed (${res.status})`);
        setScore(await res.json());
        setPhase("results");
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err));
        setPhase("results");
      }
    },
    []
  );

  const endSection = useCallback(() => {
    if (!paper) return;
    if (isLastSection) {
      submitTest(answers, paper);
    } else {
      setPhase("break");
      setDeadline(null);
    }
  }, [paper, isLastSection, answers, submitTest]);

  // Hard cutoff: when the clock hits zero the section ends on its own, with no
  // confirmation. That is the whole point of a timed test.
  const endSectionRef = useRef(endSection);
  endSectionRef.current = endSection;
  useEffect(() => {
    if (phase === "running" && deadline !== null && remaining === 0) {
      endSectionRef.current();
    }
  }, [phase, deadline, remaining]);

  function beginNextSection() {
    if (!paper) return;
    const next = sectionIndex + 1;
    setSectionIndex(next);
    setQuestionIndex(0);
    setDeadline(Date.now() + paper.sections[next].minutes * 60_000);
    setPhase("running");
  }

  const question = section?.questions[questionIndex];
  const passage =
    question?.passage_id != null
      ? section?.passages.find((p) => p.id === question.passage_id)
      : undefined;

  return (
    <main style={{ maxWidth: 900, margin: "40px auto", padding: "0 16px 60px" }}>
      <h1 style={{ marginBottom: 20 }}>Practice Test</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {phase === "idle" && (
        <div>
          {paper && (
            <div className="wood-panel" style={{ padding: 20, marginBottom: 16 }}>
              <h2 style={{ fontSize: 14, marginBottom: 12 }}>Test structure</h2>
              {paper.sections.map((s) => (
                <p key={s.label} style={{ marginBottom: 6 }}>
                  {s.label} — {s.questions.length} questions, {s.minutes} minutes
                </p>
              ))}
              {paper.warnings.length > 0 && (
                <div style={{ marginTop: 14 }}>
                  <p style={{ marginBottom: 6 }}>
                    <strong>This is a reduced-length test.</strong>
                  </p>
                  {paper.warnings.map((w, i) => (
                    <p key={i} style={{ fontSize: 13, marginBottom: 4 }}>
                      {w}
                    </p>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="wood-panel" style={{ padding: 20, marginBottom: 16 }}>
            <h2 style={{ fontSize: 14, marginBottom: 12 }}>Before you start</h2>
            <p style={{ marginBottom: 10 }}>
              Three sections, 35 minutes each. Each section ends automatically
              when its timer reaches zero — you cannot return to it.
            </p>
            <p style={{ marginBottom: 10 }}>
              You can move freely between questions within a section. Nothing is
              marked right or wrong until the whole test is submitted.
            </p>
            <p>
              This test is <strong>not saved</strong>. Reloading the page loses
              your progress.
            </p>
          </div>
          <button
            className="block-btn block-btn-primary"
            onClick={startTest}
            disabled={loading || !paper}
          >
            {loading ? "Building test..." : "Start Test"}
          </button>
        </div>
      )}

      {phase === "running" && section && question && (
        <div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: 12,
              marginBottom: 12,
              flexWrap: "wrap",
            }}
          >
            <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
              {section.label} &middot; Question {questionIndex + 1} of{" "}
              {section.questions.length} &middot; Type:{" "}
              {formatQuestionType(question.question_type)}
            </span>
            <TimerDisplay seconds={remaining} />
          </div>

          <div
            style={{
              display: "flex",
              gap: 24,
              alignItems: "flex-start",
              flexWrap: "wrap",
            }}
          >
            {passage && (
              <div
                className="clean-card"
                style={{ flex: "1 1 380px", maxHeight: 620, overflowY: "auto" }}
              >
                {passage.title && (
                  <p style={{ marginBottom: 12 }}>
                    <strong>{passage.title}</strong>
                  </p>
                )}
                {passage.passage_text.split("\n\n").map((para, i) => (
                  <p key={i} style={{ marginBottom: 12 }}>
                    {para}
                  </p>
                ))}
              </div>
            )}

            <div style={{ flex: "1 1 340px" }}>
              {/* result={null} — no feedback until the whole test is submitted */}
              <QuestionCard
                question={question}
                selected={answers[question.id] ?? null}
                onSelect={(letter) =>
                  setAnswers((prev) => ({ ...prev, [question.id]: letter }))
                }
                locked={false}
              />

              <div
                style={{ marginTop: 20, display: "flex", gap: 10, flexWrap: "wrap" }}
              >
                <button
                  className="block-btn block-btn-secondary"
                  onClick={() => setQuestionIndex((i) => Math.max(0, i - 1))}
                  disabled={questionIndex === 0}
                >
                  Previous
                </button>
                {questionIndex < section.questions.length - 1 ? (
                  <button
                    className="block-btn block-btn-primary"
                    onClick={() => setQuestionIndex((i) => i + 1)}
                  >
                    Next
                  </button>
                ) : (
                  <button
                    className="block-btn block-btn-primary"
                    onClick={endSection}
                  >
                    {isLastSection ? "Finish Test" : "Finish Section"}
                  </button>
                )}
              </div>

              <p
                style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 12 }}
              >
                Answered {section.questions.filter((q) => answers[q.id]).length} of{" "}
                {section.questions.length} in this section.
              </p>
            </div>
          </div>
        </div>
      )}

      {phase === "break" && paper && (
        <div>
          <div className="wood-panel" style={{ padding: 20, marginBottom: 16 }}>
            <h2 style={{ fontSize: 14, marginBottom: 8 }}>Section complete</h2>
            <p>
              Next: {paper.sections[sectionIndex + 1].label} —{" "}
              {paper.sections[sectionIndex + 1].questions.length} questions,{" "}
              {paper.sections[sectionIndex + 1].minutes} minutes. The timer starts
              when you continue.
            </p>
          </div>
          <button className="block-btn block-btn-primary" onClick={beginNextSection}>
            Start Next Section
          </button>
        </div>
      )}

      {phase === "grading" && <p>Grading your test...</p>}

      {phase === "results" && score && paper && (
        <div>
          <div className="wood-panel" style={{ padding: 20, marginBottom: 16 }}>
            <h2 style={{ fontSize: 14, marginBottom: 8 }}>Raw score</h2>
            <p style={{ marginBottom: 8 }}>
              <strong>
                {score.correct} of {score.total} correct
              </strong>{" "}
              ({Math.round((100 * score.correct) / score.total)}%)
            </p>
            <p style={{ fontSize: 12, color: "var(--text-muted)" }}>
              {score.total - score.answered} left blank (scored incorrect). Scaled
              120-180 scoring arrives in v0.7.
            </p>
          </div>

          {paper.sections.map((s) => {
            const ids = new Set(s.questions.map((q) => q.id));
            const inSection = score.results.filter((r) => ids.has(r.question_id));
            const right = inSection.filter((r) => r.correct).length;
            return (
              <p key={s.label} style={{ marginBottom: 6 }}>
                {s.label}: <strong>{right}</strong> / {inSection.length}
              </p>
            );
          })}

          <h2 style={{ fontSize: 14, margin: "24px 0 12px" }}>Review</h2>
          {paper.sections.flatMap((s) =>
            s.questions.map((q) => {
              const result = score.results.find((r) => r.question_id === q.id);
              if (!result) return null;
              return (
                <div key={q.id} style={{ marginBottom: 28 }}>
                  <p
                    style={{
                      fontSize: 12,
                      color: "var(--text-muted)",
                      marginBottom: 8,
                    }}
                  >
                    {s.label} &middot; {formatQuestionType(q.question_type)}
                    {result.selected_answer === null && " · left blank"}
                  </p>
                  <QuestionCard
                    question={q}
                    selected={result.selected_answer}
                    onSelect={() => {}}
                    locked
                  />
                  <div style={{ marginTop: 12 }}>
                    <GradeResultView
                      result={{
                        correct: result.correct,
                        correct_answer: result.correct_answer,
                        explanation: result.explanation,
                      }}
                    />
                  </div>
                </div>
              );
            })
          )}

          <button className="block-btn block-btn-primary" onClick={restartTest}>
            Take Another Test
          </button>
        </div>
      )}
    </main>
  );
}
