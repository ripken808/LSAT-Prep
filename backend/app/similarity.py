"""Near-duplicate detection across the question bank.

Authoring-time only — nothing here runs in the request path. The point is to
catch questions that are too much alike before they reach the bank, since
CLAUDE.md's "never memorizable" requirement is a property of the bank as a
whole and nothing else measures it.

The embedding model is imported lazily inside embed(), so importing this module
(and running the tests) never pulls PyTorch. Everything except embed() is plain
numpy over vectors you pass in, which is what makes the tests cheap.
"""

import hashlib

import numpy as np

# BAAI/bge-small-en-v1.5: 512-token context, 384 dimensions. The obvious first
# choice, all-MiniLM-L6-v2, truncates at 256 tokens — and the bank's longest
# question (a parallel-reasoning item whose five choices are each full
# arguments) is 271 tokens, so it would have been silently cut. 512 leaves
# roughly 2x headroom over the current maximum.
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384

# Cosine similarity at or above this is worth a human look.
DEFAULT_THRESHOLD = 0.80
# At or above this, treat as a duplicate and fail the check.
DEFAULT_FAIL_OVER = 0.95

_model = None


def question_text(question: dict) -> str:
    """The text representing a question for similarity purposes: its stimulus
    (LR only — RC questions carry stimulus=None), stem, and choices.

    The RC passage is deliberately EXCLUDED. Two RC questions about the same
    passage are not duplicates — they are intentionally different questions
    about shared material — so the passage is context, not identity. Including
    it was tried first and failed badly in two compounding ways: a ~555-token
    passage dwarfs a ~60-token stem, and all-MiniLM-L6-v2 truncates at 256
    tokens, so the embedded text was the first 256 tokens of the passage and
    nothing else. Every question sharing a passage scored exactly 1.000 and the
    stem and choices never reached the model at all.
    """
    parts: list[str] = []
    if question.get("stimulus"):
        parts.append(question["stimulus"])
    parts.append(question["question_stem"])
    parts.extend(question["choices"])
    return "\n".join(parts)


def content_hash(text: str) -> str:
    """Cache key. Content-addressed rather than keyed by question id, so the
    cache survives the seed script's wipe-and-reinsert (which reassigns ids)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def embed(texts: list[str]) -> np.ndarray:
    """(n, EMBEDDING_DIM) float32 array. Loads the model on first call.

    Raises if any text would be silently truncated. That failure mode is not
    theoretical: it produced identical embeddings for every RC question sharing
    a passage, and reported them as perfect duplicates, with no error at all.
    Loud failure is the only safe behavior here.
    """
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - depends on optional extra
            raise ImportError(
                "sentence-transformers is not installed. It is an optional extra "
                "because it pulls PyTorch (~2GB). Install it with:\n"
                "    cd backend && uv sync --extra dedup"
            ) from exc
        _model = SentenceTransformer(EMBEDDING_MODEL)

    limit = _model.max_seq_length
    for text in texts:
        n_tokens = len(_model.tokenizer.encode(text))
        if n_tokens > limit:
            raise ValueError(
                f"Text is {n_tokens} tokens but {EMBEDDING_MODEL} truncates at "
                f"{limit}. Everything past the cutoff is invisible to the model, "
                f"so the resulting similarity scores would be meaningless. "
                f"Shorten what gets embedded (see question_text) or switch to a "
                f"longer-context model.\nOffending text starts: {text[:120]!r}"
            )

    return np.asarray(_model.encode(texts), dtype=np.float32)


def cosine_matrix(vectors: np.ndarray) -> np.ndarray:
    """Pairwise cosine similarity. Zero vectors get a norm of 1 so they yield
    similarity 0 rather than NaN."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    normalized = vectors / norms
    return normalized @ normalized.T


def rank_pairs(
    vectors: np.ndarray, labels: list, threshold: float = 0.0
) -> list[tuple[float, object, object]]:
    """(similarity, label_a, label_b) for every distinct pair at or above
    threshold, most similar first. Upper triangle only — a pair is reported
    once, and nothing is compared to itself."""
    similarity = cosine_matrix(vectors)
    pairs = [
        (float(similarity[i, j]), labels[i], labels[j])
        for i in range(len(labels))
        for j in range(i + 1, len(labels))
        if similarity[i, j] >= threshold
    ]
    pairs.sort(key=lambda pair: -pair[0])
    return pairs
