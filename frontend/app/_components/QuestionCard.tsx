"use client";

// Shared question-rendering pieces used by all three practice flows (/,
// /reading-comp, /focus). Presentational only - each page keeps ownership of
// its own state and grading fetch, since the flows differ (one random draw vs.
// cycling a passage's questions vs. cycling a filtered set).

export type Question = {
  id: number;
  section: string;
  question_type: string;
  content_area: string | null;
  passage_id: number | null;
  stimulus: string | null; // null for RC questions - text lives on the passage
  question_stem: string;
  choices: string[];
};

export type GradeResult = {
  correct: boolean;
  correct_answer: string;
  explanation: string;
};

export const LETTERS = ["A", "B", "C", "D", "E"];

/** "rc_main_point" -> "Main Point"; the rc_ prefix is schema detail, not UI. */
export function formatQuestionType(type: string): string {
  return type
    .replace(/^rc_/, "")
    .split("_")
    .map((word) => word[0].toUpperCase() + word.slice(1))
    .join(" ");
}

type QuestionCardProps = {
  question: Question;
  selected: string | null;
  onSelect: (letter: string) => void;
  locked: boolean;
};

/** Stimulus (when present), stem and choices, in the deliberately unthemed
 *  clean-card - long-form reading content stays plain and high-contrast. */
export function QuestionCard({
  question,
  selected,
  onSelect,
  locked,
}: QuestionCardProps) {
  return (
    <div className="clean-card">
      {question.stimulus && (
        <p style={{ marginBottom: 16 }}>{question.stimulus}</p>
      )}
      <p style={{ marginBottom: 16 }}>
        <strong>{question.question_stem}</strong>
      </p>

      <form>
        {question.choices.map((choice, i) => (
          <label key={i} style={{ display: "block", margin: "10px 0" }}>
            <input
              type="radio"
              name="choice"
              value={LETTERS[i]}
              checked={selected === LETTERS[i]}
              onChange={() => onSelect(LETTERS[i])}
              disabled={locked}
            />{" "}
            ({LETTERS[i]}) {choice}
          </label>
        ))}
      </form>
    </div>
  );
}

/** Short themed correct/incorrect chip plus the stored explanation. The
 *  verdict is never conveyed by color alone - it always carries a text label,
 *  since the status green/red pair is not CVD-separable. */
export function GradeResultView({ result }: { result: GradeResult }) {
  return (
    <>
      <div
        className={`result-chip ${
          result.correct ? "result-chip-correct" : "result-chip-incorrect"
        }`}
      >
        {result.correct ? "Correct!" : "Incorrect."} Correct answer:{" "}
        {result.correct_answer}
      </div>

      <div className="clean-card" style={{ marginBottom: 16 }}>
        <p>{result.explanation}</p>
      </div>
    </>
  );
}
