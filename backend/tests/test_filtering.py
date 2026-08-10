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


def _lr_question(question_type: str, stem: str = "Stem?") -> dict:
    return {
        "section": "logical_reasoning",
        "question_type": question_type,
        "content_area": None,
        "passage_id": None,
        "stimulus": "Some stimulus.",
        "question_stem": stem,
        "choices": ["a", "b", "c", "d", "e"],
        "correct_answer": "C",
        "explanation": "Because C.",
        "verified": True,
    }


@pytest.fixture()
def seeded(db_and_client):
    """Two LR types (flaw x2, weaken x1) plus one RC question hanging off a
    law passage — enough to exercise section, type and content-area filters."""
    db_path, client = db_and_client
    with get_connection(db_path) as conn:
        insert_question(conn, _lr_question("flaw", "Flaw one?"))
        insert_question(conn, _lr_question("flaw", "Flaw two?"))
        insert_question(conn, _lr_question("weaken", "Weaken one?"))
        passage_id = insert_passage(
            conn,
            {
                "content_area": "law",
                "title": "A Law Passage",
                "passage_text": "Passage body.",
            },
        )
        insert_question(
            conn,
            {
                "section": "reading_comprehension",
                "question_type": "rc_main_point",
                "content_area": None,  # RC questions inherit the passage's area
                "passage_id": passage_id,
                "stimulus": None,
                "question_stem": "Main point?",
                "choices": ["a", "b", "c", "d", "e"],
                "correct_answer": "B",
                "explanation": "Because B.",
                "verified": True,
            },
        )
    return db_path, client


def test_taxonomy_empty_when_no_questions(db_and_client):
    _db_path, client = db_and_client
    body = client.get("/api/taxonomy").json()
    assert body == {"types": [], "content_areas": []}


def test_taxonomy_reports_counts_per_type_and_area(seeded):
    _db_path, client = seeded
    body = client.get("/api/taxonomy").json()

    counts = {(t["section"], t["question_type"]): t["count"] for t in body["types"]}
    assert counts == {
        ("logical_reasoning", "flaw"): 2,
        ("logical_reasoning", "weaken"): 1,
        ("reading_comprehension", "rc_main_point"): 1,
    }
    # Content area comes from the joined passage, not the question row.
    assert body["content_areas"] == [{"content_area": "law", "count": 1}]


def test_filter_by_single_type(seeded):
    _db_path, client = seeded
    body = client.get("/api/questions/filtered?question_type=flaw").json()
    assert body["total"] == 2
    assert {q["question_type"] for q in body["questions"]} == {"flaw"}


def test_filter_by_multiple_types_returns_union(seeded):
    _db_path, client = seeded
    body = client.get(
        "/api/questions/filtered?question_type=flaw&question_type=weaken"
    ).json()
    assert body["total"] == 3
    assert {q["question_type"] for q in body["questions"]} == {"flaw", "weaken"}


def test_filter_by_section(seeded):
    _db_path, client = seeded
    body = client.get("/api/questions/filtered?section=logical_reasoning").json()
    assert body["total"] == 3
    assert {q["section"] for q in body["questions"]} == {"logical_reasoning"}


def test_filter_by_content_area_matches_rc_through_passage_join(seeded):
    """RC questions store content_area=NULL — filtering has to reach through
    passage_id to the passage's area, or this returns nothing."""
    _db_path, client = seeded
    body = client.get("/api/questions/filtered?content_area=law").json()
    assert body["total"] == 1
    assert body["questions"][0]["question_type"] == "rc_main_point"


def test_no_filters_returns_everything(seeded):
    _db_path, client = seeded
    assert client.get("/api/questions/filtered").json()["total"] == 4


def test_unknown_type_returns_empty_set_not_error(seeded):
    _db_path, client = seeded
    response = client.get("/api/questions/filtered?question_type=does_not_exist")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "questions": []}


def test_filtered_questions_never_leak_answer_or_explanation(seeded):
    _db_path, client = seeded
    body = client.get("/api/questions/filtered").json()
    assert body["questions"]
    for question in body["questions"]:
        assert "correct_answer" not in question
        assert "explanation" not in question
