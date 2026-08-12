import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

import app.db as db_module
import app.main as main_module
from app.db import get_connection, insert_passage, insert_question
from app.assembly import PRESETS, AssemblyError, assemble_test

LR_TYPES = [
    "flaw", "weaken", "strengthen", "inference", "main_point", "principle",
    "necessary_assumption",
]


@pytest.fixture()
def db_and_client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    return db_path, TestClient(main_module.app)


def _lr(question_type: str, n: int) -> dict:
    return {
        "section": "logical_reasoning",
        "question_type": question_type,
        "content_area": None,
        "passage_id": None,
        "stimulus": f"Stimulus {n}.",
        "question_stem": f"Stem {n}?",
        "choices": ["a", "b", "c", "d", "e"],
        "correct_answer": "C",
        "explanation": "Because C.",
        "verified": True,
    }


@pytest.fixture()
def seeded(db_and_client):
    """A bank big enough for the reduced preset: 49 LR across 7 types, and
    3 passages x 5 RC questions."""
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        n = 0
        for question_type in LR_TYPES:
            for _ in range(7):
                n += 1
                insert_question(conn, _lr(question_type, n))

        for p in range(3):
            passage_id = insert_passage(
                conn,
                {
                    "content_area": "law",
                    "title": f"Passage {p}",
                    "passage_text": f"Body of passage {p}.",
                },
            )
            for q in range(5):
                insert_question(
                    conn,
                    {
                        "section": "reading_comprehension",
                        "question_type": "rc_main_point",
                        "content_area": None,
                        "passage_id": passage_id,
                        "stimulus": None,
                        "question_stem": f"Passage {p} question {q}?",
                        "choices": ["a", "b", "c", "d", "e"],
                        "correct_answer": "B",
                        "explanation": "Because B.",
                        "verified": True,
                    },
                )
    return db_path, client


def test_section_counts_match_the_preset(seeded):
    db_path, _ = seeded
    with get_connection(db_path) as conn:
        paper = assemble_test(conn, "reduced")

    counts = [len(s["questions"]) for s in paper["sections"]]
    assert counts == [s.question_count for s in PRESETS["reduced"]]


def test_no_question_appears_twice_in_a_test(seeded):
    """The core invariant: a test must never ask the same question twice, even
    across different sections."""
    db_path, _ = seeded
    with get_connection(db_path) as conn:
        paper = assemble_test(conn, "reduced")

    ids = [q["id"] for section in paper["sections"] for q in section["questions"]]
    assert len(ids) == len(set(ids))


def test_lr_section_spans_multiple_types(seeded):
    """A section of 21 shouldn't be one question type repeated."""
    db_path, _ = seeded
    with get_connection(db_path) as conn:
        paper = assemble_test(conn, "reduced")

    lr = next(s for s in paper["sections"] if s["kind"] == "logical_reasoning")
    assert len({q["question_type"] for q in lr["questions"]}) >= 5


def test_rc_section_questions_all_belong_to_its_passages(seeded):
    """RC is assembled by passage — a section must not include a question whose
    passage it never shows."""
    db_path, _ = seeded
    with get_connection(db_path) as conn:
        paper = assemble_test(conn, "reduced")

    rc = next(s for s in paper["sections"] if s["kind"] == "reading_comprehension")
    shown = {p["id"] for p in rc["passages"]}
    assert shown
    assert all(q["passage_id"] in shown for q in rc["questions"])


def test_blueprint_refuses_when_the_bank_is_too_small(seeded):
    db_path, _ = seeded
    with get_connection(db_path) as conn:
        with pytest.raises(AssemblyError) as exc:
            assemble_test(conn, "blueprint")

    # The message must name the shortfall, not just say "not enough".
    assert "short by" in str(exc.value)


def test_unknown_preset_is_rejected(seeded):
    db_path, _ = seeded
    with get_connection(db_path) as conn:
        with pytest.raises(AssemblyError):
            assemble_test(conn, "nonexistent")


def test_seed_makes_assembly_reproducible(seeded):
    db_path, _ = seeded
    with get_connection(db_path) as conn:
        first = assemble_test(conn, "reduced", seed=7)
        second = assemble_test(conn, "reduced", seed=7)

    def ids(paper):
        return [q["id"] for s in paper["sections"] for q in s["questions"]]

    assert ids(first) == ids(second)


def test_new_test_endpoint_never_leaks_answers(seeded):
    _db_path, client = seeded
    body = client.get("/api/test/new?preset=reduced").json()

    assert body["preset"] == "reduced"
    for section in body["sections"]:
        for question in section["questions"]:
            assert "correct_answer" not in question
            assert "explanation" not in question


def test_new_test_endpoint_reports_content_warnings(seeded):
    """The UI must be able to say the test is reduced rather than imply it is
    full-length."""
    _db_path, client = seeded
    body = client.get("/api/test/new?preset=reduced").json()
    assert body["warnings"]


def test_blueprint_preset_returns_400_with_the_shortfall(seeded):
    _db_path, client = seeded
    response = client.get("/api/test/new?preset=blueprint")
    assert response.status_code == 400
    assert "short by" in response.json()["detail"]


def test_grade_test_counts_correct_and_answered(seeded):
    db_path, client = seeded
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT id, correct_answer FROM questions LIMIT 3"
        ).fetchall()

    answers = [
        {"question_id": rows[0]["id"], "selected_answer": rows[0]["correct_answer"]},
        {"question_id": rows[1]["id"], "selected_answer": "A"
         if rows[1]["correct_answer"] != "A" else "B"},
        {"question_id": rows[2]["id"], "selected_answer": None},
    ]
    body = client.post("/api/test/grade", json={"answers": answers}).json()

    assert body["total"] == 3
    assert body["correct"] == 1
    assert body["answered"] == 2  # the blank doesn't count as answered


def test_unanswered_question_is_scored_incorrect(seeded):
    db_path, client = seeded
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT id FROM questions LIMIT 1").fetchone()

    body = client.post(
        "/api/test/grade",
        json={"answers": [{"question_id": row["id"], "selected_answer": None}]},
    ).json()

    assert body["correct"] == 0
    assert body["results"][0]["correct"] is False


def test_grading_a_test_records_attempts_for_answered_questions_only(seeded):
    db_path, client = seeded
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT id FROM questions LIMIT 2").fetchall()

    client.post(
        "/api/test/grade",
        json={
            "answers": [
                {"question_id": rows[0]["id"], "selected_answer": "C"},
                {"question_id": rows[1]["id"], "selected_answer": None},
            ]
        },
    )

    with get_connection(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) AS n FROM attempts").fetchone()["n"]
    assert count == 1


def test_grade_test_rejects_invalid_answer_letter(seeded):
    db_path, client = seeded
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT id FROM questions LIMIT 1").fetchone()

    response = client.post(
        "/api/test/grade",
        json={"answers": [{"question_id": row["id"], "selected_answer": "Z"}]},
    )
    assert response.status_code == 400


def test_grade_test_rejects_unknown_question_id(seeded):
    _db_path, client = seeded
    response = client.post(
        "/api/test/grade",
        json={"answers": [{"question_id": 999999, "selected_answer": "A"}]},
    )
    assert response.status_code == 404


def _answer_whole_test(client, correct_count: int) -> dict:
    """Take a real assembled paper and answer `correct_count` of it correctly."""
    paper = client.get("/api/test/new").json()
    question_ids = [q["id"] for s in paper["sections"] for q in s["questions"]]

    answers = []
    for index, question_id in enumerate(question_ids):
        # The seeded bank keys LR to "C" and RC to "B"; "A" is always wrong.
        answers.append(
            {
                "question_id": question_id,
                "selected_answer": None if index >= correct_count else "correct",
            }
        )
    # Resolve "correct" against the stored key so this works for both sections.
    graded = client.post("/api/test/grade", json={"answers": [
        {"question_id": a["question_id"], "selected_answer": None} for a in answers
    ]}).json()
    keys = {r["question_id"]: r["correct_answer"] for r in graded["results"]}
    for answer in answers:
        if answer["selected_answer"] == "correct":
            answer["selected_answer"] = keys[answer["question_id"]]

    return client.post("/api/test/grade", json={"answers": answers}).json()


def test_grading_a_full_test_returns_a_scaled_score_on_the_lsat_scale(seeded):
    _db_path, client = seeded
    body = _answer_whole_test(client, correct_count=30)

    assert 120 <= body["scaled_score"] <= 180
    assert body["percentile"]
    # 52 questions is not blueprint length, so the score is extrapolated.
    assert body["scaled_is_estimated"] is True


def test_a_perfect_full_test_scores_180_and_a_blank_one_scores_120(seeded):
    _db_path, client = seeded
    paper = client.get("/api/test/new").json()
    total = sum(len(s["questions"]) for s in paper["sections"])

    assert _answer_whole_test(client, correct_count=total)["scaled_score"] == 180
    assert _answer_whole_test(client, correct_count=0)["scaled_score"] == 120


def test_a_partial_answer_list_is_too_short_to_scale(seeded):
    db_path, client = seeded
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT id FROM questions LIMIT 3").fetchall()

    body = client.post(
        "/api/test/grade",
        json={
            "answers": [
                {"question_id": row["id"], "selected_answer": "C"} for row in rows
            ]
        },
    ).json()

    # Three questions cannot produce a meaningful 120-180 score.
    assert body["scaled_score"] is None
    assert body["percentile"] is None
