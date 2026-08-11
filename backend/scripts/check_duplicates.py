"""Report near-duplicate questions in the bank.

Run after authoring any new question, alongside export_prep_txt.py:

    cd backend && uv run --extra dedup python scripts/check_duplicates.py

Reads the canonical source files (app/mock_questions.py, app/rc_content.py),
not the database — this is an authoring-time tool, and those files are what
CLAUDE.md names canonical.

Embeddings are cached in SQLite by content hash, so re-runs only embed what
actually changed.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from app.db import get_cached_embeddings, get_connection, store_embedding
from app.mock_questions import MOCK_QUESTIONS
from app.rc_content import RC_QUESTIONS
from app.similarity import (
    DEFAULT_FAIL_OVER,
    DEFAULT_THRESHOLD,
    EMBEDDING_MODEL,
    content_hash,
    embed,
    question_text,
    rank_pairs,
)


def collect_questions() -> list[dict]:
    """Every question in the bank, each with the text to embed and a label."""
    entries: list[dict] = []

    for i, question in enumerate(MOCK_QUESTIONS):
        entries.append(
            {
                "label": f"LR[{i}] {question['question_type']}",
                "stem": question["question_stem"],
                "passage": None,
                "text": question_text(question),
            }
        )

    for i, question in enumerate(RC_QUESTIONS):
        # The passage is intentionally not embedded — see question_text().
        # Labels carry it so a flagged pair is still traceable to its passage.
        entries.append(
            {
                "label": f"RC[{i}] {question['question_type']} "
                f"({question['passage_id']})",
                "stem": question["question_stem"],
                "passage": question["passage_id"],
                "text": question_text(question),
            }
        )

    return entries


def embed_with_cache(entries: list[dict]) -> tuple[np.ndarray, int, int]:
    """(vectors, hits, misses) — only embeds text not already cached."""
    hashes = [content_hash(e["text"]) for e in entries]

    with get_connection() as conn:
        cached = get_cached_embeddings(conn, hashes, EMBEDDING_MODEL)
        missing_idx = [i for i, h in enumerate(hashes) if h not in cached]

        if missing_idx:
            fresh = embed([entries[i]["text"] for i in missing_idx])
            for slot, i in enumerate(missing_idx):
                cached[hashes[i]] = fresh[slot]
                store_embedding(conn, hashes[i], EMBEDDING_MODEL, fresh[slot])

    vectors = np.vstack([cached[h] for h in hashes])
    return vectors, len(entries) - len(missing_idx), len(missing_idx)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"report pairs at or above this (default {DEFAULT_THRESHOLD})")
    parser.add_argument("--fail-over", type=float, default=DEFAULT_FAIL_OVER,
                        help=f"exit 1 if any pair reaches this (default {DEFAULT_FAIL_OVER})")
    parser.add_argument("--top", type=int, default=0,
                        help="also print the N most similar pairs regardless of threshold")
    args = parser.parse_args()

    entries = collect_questions()
    print(f"Bank: {len(entries)} questions "
          f"({len(MOCK_QUESTIONS)} LR + {len(RC_QUESTIONS)} RC)")

    vectors, hits, misses = embed_with_cache(entries)
    print(f"Embeddings: {hits} cached, {misses} newly computed "
          f"({EMBEDDING_MODEL})\n")

    labels = [e["label"] for e in entries]
    stems = {e["label"]: e["stem"] for e in entries}
    passages = {e["label"]: e.get("passage") for e in entries}
    all_pairs = rank_pairs(vectors, labels)

    def same_passage(a: str, b: str) -> bool:
        """Two RC questions about one passage share vocabulary by design. They
        score high and are NOT duplicates — annotate so they don't read as
        findings."""
        return passages[a] is not None and passages[a] == passages[b]

    def show(pairs, heading):
        print(heading)
        if not pairs:
            print("  (none)\n")
            return
        for score, a, b in pairs:
            note = "  [same passage — expected]" if same_passage(a, b) else ""
            print(f"  {score:.3f}  {a}{note}")
            print(f"         {stems[a][:78]}")
            print(f"         {b}")
            print(f"         {stems[b][:78]}\n")

    if args.top:
        show(all_pairs[: args.top], f"Top {args.top} most similar pairs:")

    flagged = [p for p in all_pairs if p[0] >= args.threshold]
    show(flagged, f"Pairs at or above {args.threshold}:")

    failures = [
        p for p in all_pairs
        if p[0] >= args.fail_over and not same_passage(p[1], p[2])
    ]
    if failures:
        print(f"FAIL: {len(failures)} pair(s) at or above {args.fail_over} "
              f"— treat these as duplicates.")
        return 1

    print(f"OK: no pair reaches {args.fail_over}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
