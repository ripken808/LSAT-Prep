import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator

from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS passages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_area TEXT NOT NULL,
    title TEXT,
    passage_text TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    question_type TEXT NOT NULL,
    content_area TEXT,
    passage_id INTEGER,
    stimulus TEXT,
    question_stem TEXT NOT NULL,
    choices TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (passage_id) REFERENCES passages(id)
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
            (section, question_type, content_area, passage_id, stimulus,
             question_stem, choices, correct_answer, explanation, verified,
             created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question["section"],
            question["question_type"],
            question.get("content_area"),
            question.get("passage_id"),
            question.get("stimulus"),
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
    """Random LR question (no attached passage) — used by the LR practice flow."""
    return conn.execute(
        "SELECT * FROM questions WHERE passage_id IS NULL ORDER BY RANDOM() LIMIT 1"
    ).fetchone()


def get_questions_filtered(
    conn: sqlite3.Connection,
    section: str | None = None,
    question_types: list[str] | None = None,
    content_areas: list[str] | None = None,
) -> list[sqlite3.Row]:
    """All questions matching the given filters, in random order.

    Content area is matched on COALESCE(q.content_area, p.content_area): RC
    questions carry no area of their own, so they inherit their passage's.
    Only placeholders are interpolated into the SQL below - every filter value
    stays a bound parameter.
    """
    clauses: list[str] = []
    params: list[str] = []

    if section:
        clauses.append("q.section = ?")
        params.append(section)
    if question_types:
        clauses.append(
            f"q.question_type IN ({', '.join('?' for _ in question_types)})"
        )
        params.extend(question_types)
    if content_areas:
        clauses.append(
            "COALESCE(q.content_area, p.content_area) IN "
            f"({', '.join('?' for _ in content_areas)})"
        )
        params.extend(content_areas)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return conn.execute(
        f"""
        SELECT q.* FROM questions q
        LEFT JOIN passages p ON q.passage_id = p.id
        {where}
        ORDER BY RANDOM()
        """,
        params,
    ).fetchall()


def get_taxonomy_counts(
    conn: sqlite3.Connection,
) -> tuple[list[sqlite3.Row], list[sqlite3.Row]]:
    """(types, content_areas) with counts — drives the filter UI's options so
    they can never drift from what's actually in the bank."""
    type_rows = conn.execute(
        """
        SELECT section, question_type, COUNT(*) AS count
        FROM questions
        GROUP BY section, question_type
        ORDER BY section, question_type
        """
    ).fetchall()
    content_area_rows = conn.execute(
        """
        SELECT COALESCE(q.content_area, p.content_area) AS content_area,
               COUNT(*) AS count
        FROM questions q
        LEFT JOIN passages p ON q.passage_id = p.id
        WHERE COALESCE(q.content_area, p.content_area) IS NOT NULL
        -- group/order by ordinal: bare `content_area` is ambiguous here, since
        -- both questions and passages have a column by that name
        GROUP BY 1
        ORDER BY 1
        """
    ).fetchall()
    return type_rows, content_area_rows


def get_question_by_id(conn: sqlite3.Connection, question_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM questions WHERE id = ?", (question_id,)
    ).fetchone()


def insert_passage(conn: sqlite3.Connection, passage: dict) -> int:
    cursor = conn.execute(
        """
        INSERT INTO passages (content_area, title, passage_text, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            passage["content_area"],
            passage.get("title"),
            passage["passage_text"],
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    return cursor.lastrowid


def get_random_passage(conn: sqlite3.Connection) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM passages ORDER BY RANDOM() LIMIT 1"
    ).fetchone()


def get_questions_by_passage_id(
    conn: sqlite3.Connection, passage_id: int
) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM questions WHERE passage_id = ? ORDER BY id",
        (passage_id,),
    ).fetchall()


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
