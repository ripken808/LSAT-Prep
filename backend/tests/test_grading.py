import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

import app.db as db_module
import app.main as main_module
from app.db import get_connection, insert_question


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    return TestClient(main_module.app)


@pytest.fixture()
def seeded_question_id(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    with get_connection(db_path) as conn:
        question_id = insert_question(
            conn,
            {
                "section": "logical_reasoning",
                "question_type": "necessary_assumption",
                "content_area": None,
                "stimulus": "Test stimulus.",
                "question_stem": "Which one of the following is an assumption?",
                "choices": ["A text", "B text", "C text", "D text", "E text"],
                "correct_answer": "C",
                "explanation": "Negation test explanation.",
                "verified": True,
            },
        )
    return db_path, question_id


def test_grade_correct_answer(monkeypatch, seeded_question_id):
    db_path, question_id = seeded_question_id
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    client = TestClient(main_module.app)

    response = client.post(
        f"/api/question/{question_id}/grade", json={"selected_answer": "C"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["correct"] is True
    assert body["correct_answer"] == "C"
    assert body["explanation"] == "Negation test explanation."


def test_grade_incorrect_answer(monkeypatch, seeded_question_id):
    db_path, question_id = seeded_question_id
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    client = TestClient(main_module.app)

    response = client.post(
        f"/api/question/{question_id}/grade", json={"selected_answer": "A"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["correct"] is False
    assert body["correct_answer"] == "C"
    # Explanation is still shown after grading, regardless of correctness.
    assert body["explanation"] == "Negation test explanation."


def test_grade_invalid_answer_letter(monkeypatch, seeded_question_id):
    db_path, question_id = seeded_question_id
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    client = TestClient(main_module.app)

    response = client.post(
        f"/api/question/{question_id}/grade", json={"selected_answer": "Z"}
    )
    assert response.status_code == 400


def test_grade_unknown_question_id(monkeypatch, tmp_path):
    db_path = tmp_path / "empty.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    client = TestClient(main_module.app)

    response = client.post("/api/question/999/grade", json={"selected_answer": "A"})
    assert response.status_code == 404


def test_get_current_question(monkeypatch, seeded_question_id):
    db_path, question_id = seeded_question_id
    monkeypatch.setattr(main_module, "get_connection", lambda: get_connection(db_path))
    client = TestClient(main_module.app)

    response = client.get("/api/question/current")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == question_id
    assert "correct_answer" not in body
    assert "explanation" not in body
    assert len(body["choices"]) == 5
