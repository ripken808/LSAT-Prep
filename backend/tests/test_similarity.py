"""Tests for the near-duplicate check.

Deliberately never call similarity.embed() or import sentence_transformers:
the model is an optional extra that pulls PyTorch, and the test suite must run
without it. Everything here feeds hand-built vectors to the pure functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest

import app.db as db_module
from app.db import get_cached_embeddings, get_connection, store_embedding
from app.similarity import (
    EMBEDDING_MODEL,
    content_hash,
    cosine_matrix,
    question_text,
    rank_pairs,
)


@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", path)
    return path


def test_identical_vectors_are_similarity_one():
    vectors = np.array([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], dtype=np.float32)
    assert cosine_matrix(vectors)[0, 1] == pytest.approx(1.0)


def test_orthogonal_vectors_are_similarity_zero():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    assert cosine_matrix(vectors)[0, 1] == pytest.approx(0.0)


def test_magnitude_does_not_affect_similarity():
    """Cosine compares direction — a longer question isn't less similar."""
    vectors = np.array([[1.0, 1.0], [50.0, 50.0]], dtype=np.float32)
    assert cosine_matrix(vectors)[0, 1] == pytest.approx(1.0)


def test_zero_vector_yields_zero_not_nan():
    vectors = np.array([[0.0, 0.0], [1.0, 1.0]], dtype=np.float32)
    similarity = cosine_matrix(vectors)
    assert not np.isnan(similarity).any()
    assert similarity[0, 1] == pytest.approx(0.0)


def test_rank_pairs_orders_most_similar_first():
    vectors = np.array(
        [[1.0, 0.0], [1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], dtype=np.float32
    )
    pairs = rank_pairs(vectors, ["a", "b", "c", "d"])
    scores = [score for score, _, _ in pairs]
    assert scores == sorted(scores, reverse=True)
    # The two identical vectors are the closest pair.
    assert {pairs[0][1], pairs[0][2]} == {"a", "b"}


def test_rank_pairs_reports_each_pair_once_and_never_self():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=np.float32)
    pairs = rank_pairs(vectors, ["a", "b", "c"])
    assert len(pairs) == 3  # 3 choose 2
    for _, first, second in pairs:
        assert first != second


def test_rank_pairs_threshold_filters():
    vectors = np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    assert len(rank_pairs(vectors, ["a", "b", "c"], threshold=0.99)) == 1
    assert len(rank_pairs(vectors, ["a", "b", "c"], threshold=-1.0)) == 3


def test_question_text_includes_stimulus_stem_and_choices():
    question = {
        "stimulus": "STIMULUS-MARKER",
        "question_stem": "STEM-MARKER",
        "choices": ["one", "two", "three", "four", "five"],
    }
    text = question_text(question)
    for marker in ("STIMULUS-MARKER", "STEM-MARKER", "three"):
        assert marker in text


def test_question_text_excludes_passage_for_rc():
    """Two RC questions about one passage are not duplicates. Embedding the
    passage made them score exactly 1.000 — it dwarfs the stem AND overflows the
    model's 256-token limit, so only passage text ever reached the model."""
    rc_question = {
        "stimulus": None,
        "question_stem": "STEM-MARKER",
        "choices": ["a", "b", "c", "d", "e"],
    }
    text = question_text(rc_question)
    assert "STEM-MARKER" in text
    assert text.startswith("STEM-MARKER")  # no stimulus, so the stem leads


def test_content_hash_is_stable_and_distinguishing():
    assert content_hash("same") == content_hash("same")
    assert content_hash("same") != content_hash("different")


def test_embedding_survives_sqlite_blob_round_trip(db_path):
    vector = np.array([0.1, -0.2, 0.3], dtype=np.float32)
    with get_connection(db_path) as conn:
        store_embedding(conn, "hash-a", EMBEDDING_MODEL, vector)

    with get_connection(db_path) as conn:
        cached = get_cached_embeddings(conn, ["hash-a"], EMBEDDING_MODEL)

    assert np.allclose(cached["hash-a"], vector)


def test_cache_lookup_returns_only_known_hashes(db_path):
    with get_connection(db_path) as conn:
        store_embedding(
            conn, "known", EMBEDDING_MODEL, np.array([1.0], dtype=np.float32)
        )
        cached = get_cached_embeddings(conn, ["known", "unknown"], EMBEDDING_MODEL)

    assert set(cached) == {"known"}


def test_cache_is_scoped_by_model(db_path):
    """Swapping the embedding model must not silently reuse the old vectors."""
    with get_connection(db_path) as conn:
        store_embedding(
            conn, "hash-a", EMBEDDING_MODEL, np.array([1.0], dtype=np.float32)
        )
        assert get_cached_embeddings(conn, ["hash-a"], "some-other-model") == {}


def test_empty_hash_list_short_circuits(db_path):
    with get_connection(db_path) as conn:
        assert get_cached_embeddings(conn, [], EMBEDDING_MODEL) == {}
