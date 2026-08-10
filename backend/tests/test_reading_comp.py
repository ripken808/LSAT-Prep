import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

import app.db as db_module
import app.main as main_module
from app.db import get_connection, insert_passage, insert_question


@pytest.fixture()
def db_and_client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    return db_path, TestClient(main_module.app)


def test_passage_random_404_when_empty(db_and_client):
    _db_path, client = db_and_client
    response = client.get("/api/passage/random")
    assert response.status_code == 404


def test_passage_random_returns_passage_and_questions(db_and_client):
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        passage_id = insert_passage(
            conn,
            {
                "content_area": "law",
                "title": "Test Passage",
                "passage_text": "Some passage text.",
            },
        )
        insert_question(
            conn,
            {
                "section": "reading_comprehension",
                "question_type": "rc_main_point",
                "content_area": "law",
                "passage_id": passage_id,
                "stimulus": None,
                "question_stem": "What is the main point?",
                "choices": ["A", "B", "C", "D", "E"],
                "correct_answer": "B",
                "explanation": "Because B.",
                "verified": True,
            },
        )

    response = client.get("/api/passage/random")
    assert response.status_code == 200
    body = response.json()
    assert body["passage"]["title"] == "Test Passage"
    assert body["passage"]["content_area"] == "law"
    assert len(body["questions"]) == 1
    assert body["questions"][0]["question_type"] == "rc_main_point"
    assert body["questions"][0]["passage_id"] == passage_id
    # Answer/explanation never leak in the public question payload.
    assert "correct_answer" not in body["questions"][0]
    assert "explanation" not in body["questions"][0]


def test_grading_works_for_rc_question(db_and_client):
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        passage_id = insert_passage(
            conn,
            {"content_area": "law", "title": "T", "passage_text": "Text."},
        )
        question_id = insert_question(
            conn,
            {
                "section": "reading_comprehension",
                "question_type": "rc_specific_detail",
                "content_area": "law",
                "passage_id": passage_id,
                "stimulus": None,
                "question_stem": "Detail?",
                "choices": ["A", "B", "C", "D", "E"],
                "correct_answer": "D",
                "explanation": "Stated explicitly.",
                "verified": True,
            },
        )

    response = client.post(
        f"/api/question/{question_id}/grade", json={"selected_answer": "D"}
    )
    assert response.status_code == 200
    assert response.json()["correct"] is True


def test_lr_random_endpoint_excludes_rc_questions(db_and_client):
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        passage_id = insert_passage(
            conn,
            {"content_area": "law", "title": "T", "passage_text": "Text."},
        )
        insert_question(
            conn,
            {
                "section": "reading_comprehension",
                "question_type": "rc_inference",
                "content_area": "law",
                "passage_id": passage_id,
                "stimulus": None,
                "question_stem": "Infer?",
                "choices": ["A", "B", "C", "D", "E"],
                "correct_answer": "A",
                "explanation": "Entailed.",
                "verified": True,
            },
        )
        insert_question(
            conn,
            {
                "section": "logical_reasoning",
                "question_type": "flaw",
                "content_area": None,
                "stimulus": "An LR stimulus.",
                "question_stem": "What's the flaw?",
                "choices": ["A", "B", "C", "D", "E"],
                "correct_answer": "A",
                "explanation": "Named flaw.",
                "verified": True,
            },
        )

    for _ in range(10):
        response = client.get("/api/question/current")
        assert response.status_code == 200
        assert response.json()["section"] == "logical_reasoning"
