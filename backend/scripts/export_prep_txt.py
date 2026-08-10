"""Export the full hand-authored question bank (LR + RC) to a plain-text
study file at the repo root: prep.txt.

Regenerates from the canonical source files (app/mock_questions.py,
app/rc_content.py) — never hand-edit prep.txt directly, it will be
overwritten. Per CLAUDE.md's Workflow Notes: run this any time a new
question is authored/verified, so prep.txt stays in sync.

Usage: uv run python scripts/export_prep_txt.py
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.mock_questions import MOCK_QUESTIONS
from app.rc_content import PASSAGES, RC_QUESTIONS

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_PATH = REPO_ROOT / "prep.txt"

LETTERS = ["A", "B", "C", "D", "E"]
THICK_RULE = "=" * 80
THIN_RULE = "-" * 80


def format_question_type(question_type: str) -> str:
    return question_type.removeprefix("rc_").replace("_", " ").title()


def format_choices(choices: list[str]) -> str:
    return "\n".join(f"({letter}) {text}" for letter, text in zip(LETTERS, choices))


def format_lr_question(number: int, question: dict) -> str:
    return (
        f"{THIN_RULE}\n"
        f"[{number}] Type: {format_question_type(question['question_type'])}\n"
        f"{THIN_RULE}\n"
        f"Stimulus:\n{question['stimulus']}\n\n"
        f"Question: {question['question_stem']}\n\n"
        f"{format_choices(question['choices'])}\n\n"
        f"Correct Answer: {question['correct_answer']}\n\n"
        f"Explanation:\n{question['explanation']}\n"
    )


def format_rc_question(number: int, question: dict) -> str:
    return (
        f"{THIN_RULE}\n"
        f"[Q{number}] Type: {format_question_type(question['question_type'])}\n"
        f"{THIN_RULE}\n"
        f"Question: {question['question_stem']}\n\n"
        f"{format_choices(question['choices'])}\n\n"
        f"Correct Answer: {question['correct_answer']}\n\n"
        f"Explanation:\n{question['explanation']}\n"
    )


def build_prep_txt() -> str:
    parts = [
        THICK_RULE,
        "LSAT PREP -- Question Bank Export",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Logical Reasoning: {len(MOCK_QUESTIONS)} questions | "
        f"Reading Comprehension: {len(PASSAGES)} passages, {len(RC_QUESTIONS)} questions",
        THICK_RULE,
        "",
        "",
        "#" * 44,
        "# LOGICAL REASONING",
        "#" * 44,
        "",
    ]

    for i, question in enumerate(MOCK_QUESTIONS, start=1):
        parts.append(format_lr_question(i, question))
        parts.append("")

    parts += [
        "",
        "#" * 44,
        "# READING COMPREHENSION",
        "#" * 44,
        "",
    ]

    for p_num, passage in enumerate(PASSAGES, start=1):
        parts.append(THICK_RULE)
        parts.append(
            f"PASSAGE {p_num} ({passage['content_area']}): "
            f"{passage.get('title') or '(untitled)'}"
        )
        parts.append(THICK_RULE)
        parts.append(passage["passage_text"])
        parts.append("")

        passage_questions = [
            q for q in RC_QUESTIONS if q["passage_id"] == passage["id"]
        ]
        for q_num, question in enumerate(passage_questions, start=1):
            parts.append(format_rc_question(q_num, question))
            parts.append("")

    return "\n".join(parts)


def main():
    OUTPUT_PATH.write_text(build_prep_txt())
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
