import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

import app.db as db_module
import app.main as main_module
from app.db import get_connection, insert_question


def _question(question_type, correct_answer):
    return {
        "section": "logical_reasoning",
        "question_type": question_type,
        "content_area": None,
        "stimulus": "Test stimulus.",
        "question_stem": "Test stem?",
        "choices": ["A text", "B text", "C text", "D text", "E text"],
        "correct_answer": correct_answer,
        "explanation": "Test explanation.",
        "verified": True,
    }


@pytest.fixture()
def db_and_client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    return db_path, TestClient(main_module.app)


def test_stats_summary_empty(db_and_client):
    _db_path, client = db_and_client

    response = client.get("/api/stats/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["overall"] == {"total": 0, "correct": 0, "accuracy": None}
    assert body["by_type"] == []
    assert body["over_time"] == []


def test_grading_records_attempt(db_and_client):
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        qid = insert_question(conn, _question("necessary_assumption", "C"))

    client.post(f"/api/question/{qid}/grade", json={"selected_answer": "C"})

    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM attempts").fetchall()
    assert len(rows) == 1
    assert rows[0]["question_id"] == qid
    assert rows[0]["selected_answer"] == "C"
    assert rows[0]["correct"] == 1
    assert rows[0]["explanation_viewed"] == 1


def test_failed_grade_requests_do_not_record_attempts(db_and_client):
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        qid = insert_question(conn, _question("necessary_assumption", "C"))

    client.post(f"/api/question/{qid}/grade", json={"selected_answer": "Z"})  # invalid letter, 400
    client.post("/api/question/999/grade", json={"selected_answer": "A"})  # unknown id, 404

    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM attempts").fetchall()
    assert len(rows) == 0


def test_stats_summary_aggregates_across_types_and_attempts(db_and_client):
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        na_id = insert_question(conn, _question("necessary_assumption", "C"))
        flaw_id = insert_question(conn, _question("flaw", "A"))

    # necessary_assumption: 1 correct, 1 incorrect
    client.post(f"/api/question/{na_id}/grade", json={"selected_answer": "C"})
    client.post(f"/api/question/{na_id}/grade", json={"selected_answer": "B"})
    # flaw: 1 correct
    client.post(f"/api/question/{flaw_id}/grade", json={"selected_answer": "A"})

    response = client.get("/api/stats/summary")
    assert response.status_code == 200
    body = response.json()

    assert body["overall"]["total"] == 3
    assert body["overall"]["correct"] == 2
    assert body["overall"]["accuracy"] == pytest.approx(2 / 3)

    by_type = {row["question_type"]: row for row in body["by_type"]}
    assert by_type["necessary_assumption"]["total"] == 2
    assert by_type["necessary_assumption"]["correct"] == 1
    assert by_type["necessary_assumption"]["accuracy"] == pytest.approx(0.5)
    assert by_type["flaw"]["total"] == 1
    assert by_type["flaw"]["correct"] == 1
    assert by_type["flaw"]["accuracy"] == pytest.approx(1.0)

    assert len(body["over_time"]) == 1  # all attempts happened today
    assert body["over_time"][0]["count"] == 3
