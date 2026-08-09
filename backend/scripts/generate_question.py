"""Seed the database with a Logical Reasoning question.

Behavior is controlled by GENERATION_MODE (see app/config.py):
  - "mock" (default): inserts the hand-authored static questions from
    app/mock_questions.py. No ANTHROPIC_API_KEY or network access required.
  - "live": calls the real generate_and_verify() pipeline against the
    Anthropic API (unchanged from the original live-mode implementation).

Usage: uv run python scripts/generate_question.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import GENERATION_MODE
from app.db import get_connection, get_question_by_id, insert_question
from app.generation import GenerationError, generate_and_verify
from app.mock_questions import MOCK_QUESTIONS


def seed_mock():
    print(f"GENERATION_MODE=mock - seeding {len(MOCK_QUESTIONS)} static question(s), no API calls.")
    with get_connection() as conn:
        conn.execute("DELETE FROM questions")
        for question in MOCK_QUESTIONS:
            question_id = insert_question(conn, question)
            row = get_question_by_id(conn, question_id)
            print(f"Stored question id={question_id} type={row['question_type']}")
    print("Done. GET /api/question/current will serve the most recently inserted question.")


def seed_live():
    print("GENERATION_MODE=live - generating and independently verifying a question via the Anthropic API...")
    try:
        question = generate_and_verify()
    except GenerationError as exc:
        print(f"FAILED: {exc}")
        raise SystemExit(1)

    with get_connection() as conn:
        question_id = insert_question(conn, question)
        row = get_question_by_id(conn, question_id)

    print(f"Stored question id={question_id}, verified={bool(row['verified'])}")
    print(f"Type: {row['question_type']}")
    print(f"Stimulus: {row['stimulus']}")
    print(f"Stem: {row['question_stem']}")
    print(f"Correct answer: {row['correct_answer']}")
    print(f"Explanation: {row['explanation']}")


def main():
    if GENERATION_MODE == "live":
        seed_live()
    else:
        seed_mock()


if __name__ == "__main__":
    main()
