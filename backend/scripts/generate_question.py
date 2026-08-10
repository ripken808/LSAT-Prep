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
from app.db import (
    get_connection,
    get_question_by_id,
    insert_passage,
    insert_question,
)
from app.generation import GenerationError, generate_and_verify
from app.mock_questions import MOCK_QUESTIONS
from app.rc_content import PASSAGES, RC_QUESTIONS


def seed_mock():
    print(f"GENERATION_MODE=mock - seeding {len(MOCK_QUESTIONS)} LR question(s), "
          f"{len(PASSAGES)} RC passage(s), {len(RC_QUESTIONS)} RC question(s), no API calls.")
    with get_connection() as conn:
        conn.execute("DELETE FROM questions")
        conn.execute("DELETE FROM passages")

        for question in MOCK_QUESTIONS:
            question_id = insert_question(conn, question)
            row = get_question_by_id(conn, question_id)
            print(f"Stored LR question id={question_id} type={row['question_type']}")

        passage_id_map = {}
        for passage in PASSAGES:
            db_id = insert_passage(conn, passage)
            passage_id_map[passage["id"]] = db_id
            print(f"Stored passage id={db_id} ({passage['content_area']}): {passage['title']}")

        for question in RC_QUESTIONS:
            question_id = insert_question(
                conn,
                {
                    "section": "reading_comprehension",
                    "question_type": question["question_type"],
                    "content_area": next(
                        p["content_area"] for p in PASSAGES if p["id"] == question["passage_id"]
                    ),
                    "passage_id": passage_id_map[question["passage_id"]],
                    "stimulus": None,
                    "question_stem": question["question_stem"],
                    "choices": question["choices"],
                    "correct_answer": question["correct_answer"],
                    "explanation": question["explanation"],
                    "verified": question["verified"],
                },
            )
            row = get_question_by_id(conn, question_id)
            print(f"Stored RC question id={question_id} type={row['question_type']}")
    print("Done. GET /api/question/current serves a random LR question; "
          "GET /api/passage/random serves a random RC passage + its questions.")


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
