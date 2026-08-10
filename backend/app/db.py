import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator

from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    question_type TEXT NOT NULL,
    content_area TEXT,
    stimulus TEXT NOT NULL,
    question_stem TEXT NOT NULL,
    choices TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    selected_answer TEXT NOT NULL,
    correct INTEGER NOT NULL,
    explanation_viewed INTEGER NOT NULL DEFAULT 0,
    answered_at TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
"""


@contextmanager
def get_connection(db_path=None) -> Iterator[sqlite3.Connection]:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_question(conn: sqlite3.Connection, question: dict) -> int:
    cursor = conn.execute(
        """
        INSERT INTO questions
            (section, question_type, content_area, stimulus, question_stem,
             choices, correct_answer, explanation, verified, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question["section"],
            question["question_type"],
            question.get("content_area"),
            question["stimulus"],
            question["question_stem"],
            json.dumps(question["choices"]),
            question["correct_answer"],
            question["explanation"],
            1 if question["verified"] else 0,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    return cursor.lastrowid


def get_random_question(conn: sqlite3.Connection) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM questions ORDER BY RANDOM() LIMIT 1"
    ).fetchone()


def get_question_by_id(conn: sqlite3.Connection, question_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM questions WHERE id = ?", (question_id,)
    ).fetchone()


def insert_attempt(
    conn: sqlite3.Connection,
    question_id: int,
    selected_answer: str,
    correct: bool,
    explanation_viewed: bool,
) -> int:
    """Pure logging side effect of grading — never read by the grading logic
    itself, never influences the deterministic key-match result."""
    cursor = conn.execute(
        """
        INSERT INTO attempts
            (question_id, selected_answer, correct, explanation_viewed, answered_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            question_id,
            selected_answer,
            1 if correct else 0,
            1 if explanation_viewed else 0,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    return cursor.lastrowid


def get_overall_stats(conn: sqlite3.Connection) -> sqlite3.Row:
    return conn.execute(
        "SELECT COUNT(*) AS total, COALESCE(SUM(correct), 0) AS correct FROM attempts"
    ).fetchone()


def get_stats_by_type(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT q.question_type AS question_type,
               COUNT(*) AS total,
               COALESCE(SUM(a.correct), 0) AS correct
        FROM attempts a
        JOIN questions q ON a.question_id = q.id
        GROUP BY q.question_type
        ORDER BY q.question_type
        """
    ).fetchall()


def get_attempts_by_day(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT substr(answered_at, 1, 10) AS date, COUNT(*) AS count
        FROM attempts
        GROUP BY date
        ORDER BY date
        """
    ).fetchall()
