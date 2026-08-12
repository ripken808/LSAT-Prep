"""Assemble a full-length timed practice test from the question bank.

Section sizes are configurable because the bank cannot fill a real blueprint
yet: the real LSAT is 2 LR sections of 24-26 plus an RC section of 26-28 across
4 passages, and the bank holds 42 LR and 10 RC across 2 passages. The "reduced"
preset is sized so no question repeats; "blueprint" exists and refuses with a
countable error until the content is there, rather than silently serving a
half-test or reusing questions.
"""

import random
import sqlite3
from dataclasses import dataclass

from app.db import get_questions_by_passage_id, get_questions_filtered

LOGICAL_REASONING = "logical_reasoning"
READING_COMPREHENSION = "reading_comprehension"


class AssemblyError(Exception):
    """Not enough content to build the requested test."""


@dataclass(frozen=True)
class SectionSpec:
    kind: str
    label: str
    question_count: int
    minutes: int = 35


PRESETS: dict[str, list[SectionSpec]] = {
    # Sized to what the bank actually supports, with nothing repeated.
    "reduced": [
        SectionSpec(LOGICAL_REASONING, "Section 1 — Logical Reasoning", 21),
        SectionSpec(LOGICAL_REASONING, "Section 2 — Logical Reasoning", 21),
        SectionSpec(READING_COMPREHENSION, "Section 3 — Reading Comprehension", 10),
    ],
    # The real thing. Refuses until the bank can fill it.
    "blueprint": [
        SectionSpec(LOGICAL_REASONING, "Section 1 — Logical Reasoning", 25),
        SectionSpec(LOGICAL_REASONING, "Section 2 — Logical Reasoning", 25),
        SectionSpec(READING_COMPREHENSION, "Section 3 — Reading Comprehension", 27),
    ],
}

DEFAULT_PRESET = "reduced"


def _spread_by_type(rows: list[sqlite3.Row], rng: random.Random) -> list[sqlite3.Row]:
    """Round-robin across question_type so a section isn't five flaw questions
    in a row. Within a type the order is shuffled."""
    by_type: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        by_type.setdefault(row["question_type"], []).append(row)
    for bucket in by_type.values():
        rng.shuffle(bucket)

    ordered: list[sqlite3.Row] = []
    type_names = sorted(by_type)
    rng.shuffle(type_names)
    while any(by_type[name] for name in type_names):
        for name in type_names:
            if by_type[name]:
                ordered.append(by_type[name].pop())
    return ordered


def _assemble_lr(
    specs: list[SectionSpec], conn: sqlite3.Connection, rng: random.Random
) -> list[list[sqlite3.Row]]:
    """LR sections, drawn without replacement across the WHOLE test."""
    needed = sum(spec.question_count for spec in specs)
    # get_questions_filtered returns rows ORDER BY RANDOM(), so sort to a stable
    # order first — otherwise the seeded RNG below can't make a test reproducible.
    available = sorted(
        get_questions_filtered(conn, section=LOGICAL_REASONING),
        key=lambda row: row["id"],
    )
    if len(available) < needed:
        raise AssemblyError(
            f"Not enough Logical Reasoning questions: need {needed}, "
            f"have {len(available)} (short by {needed - len(available)})."
        )

    pool = _spread_by_type(available, rng)
    sections: list[list[sqlite3.Row]] = []
    cursor = 0
    for spec in specs:
        sections.append(pool[cursor : cursor + spec.question_count])
        cursor += spec.question_count
    return sections


def _assemble_rc(
    specs: list[SectionSpec], conn: sqlite3.Connection, rng: random.Random
) -> list[tuple[list[sqlite3.Row], list[sqlite3.Row]]]:
    """RC sections as (passages, questions).

    Assembled by PASSAGE, not by question: an RC section is whole passages plus
    all of their questions, because a passage is read once and answered against
    several times. Taking N questions at random would strand questions from
    passages the test never shows.
    """
    passage_rows = conn.execute("SELECT * FROM passages ORDER BY id").fetchall()
    passages = list(passage_rows)
    rng.shuffle(passages)

    sections: list[tuple[list[sqlite3.Row], list[sqlite3.Row]]] = []
    used: set[int] = set()

    for spec in specs:
        chosen_passages: list[sqlite3.Row] = []
        chosen_questions: list[sqlite3.Row] = []
        for passage in passages:
            if passage["id"] in used:
                continue
            if len(chosen_questions) >= spec.question_count:
                break
            questions = get_questions_by_passage_id(conn, passage["id"])
            if not questions:
                continue
            chosen_passages.append(passage)
            chosen_questions.extend(questions)
            used.add(passage["id"])

        if len(chosen_questions) < spec.question_count:
            raise AssemblyError(
                f"Not enough Reading Comprehension content: need "
                f"{spec.question_count} questions, have {len(chosen_questions)} "
                f"across {len(chosen_passages)} passage(s) "
                f"(short by {spec.question_count - len(chosen_questions)})."
            )

        sections.append((chosen_passages, chosen_questions))

    return sections


def assemble_test(
    conn: sqlite3.Connection, preset: str = DEFAULT_PRESET, seed: int | None = None
) -> dict:
    """Build a test. Raises TestAssemblyError when the bank can't fill it.

    No question appears twice anywhere in the returned test — LR is drawn
    without replacement across all LR sections, and RC passages are consumed
    once.
    """
    if preset not in PRESETS:
        raise AssemblyError(
            f"Unknown preset {preset!r}. Available: {', '.join(sorted(PRESETS))}."
        )

    specs = PRESETS[preset]
    rng = random.Random(seed)

    lr_specs = [s for s in specs if s.kind == LOGICAL_REASONING]
    rc_specs = [s for s in specs if s.kind == READING_COMPREHENSION]
    lr_sections = _assemble_lr(lr_specs, conn, rng)
    rc_sections = _assemble_rc(rc_specs, conn, rng)

    lr_iter, rc_iter = iter(lr_sections), iter(rc_sections)
    sections = []
    for spec in specs:
        if spec.kind == LOGICAL_REASONING:
            questions, passages = next(lr_iter), []
        else:
            passages, questions = next(rc_iter)
        sections.append(
            {
                "kind": spec.kind,
                "label": spec.label,
                "minutes": spec.minutes,
                "passages": passages,
                "questions": questions,
            }
        )

    return {"preset": preset, "sections": sections}


def content_warnings(conn: sqlite3.Connection) -> list[str]:
    """Plain statements of where the bank falls short of the real blueprint, so
    the UI can say so rather than implying the test is blueprint-accurate."""
    blueprint = PRESETS["blueprint"]
    lr_needed = sum(s.question_count for s in blueprint if s.kind == LOGICAL_REASONING)
    rc_needed = sum(
        s.question_count for s in blueprint if s.kind == READING_COMPREHENSION
    )

    lr_have = len(get_questions_filtered(conn, section=LOGICAL_REASONING))
    rc_have = len(get_questions_filtered(conn, section=READING_COMPREHENSION))
    passages_have = conn.execute("SELECT COUNT(*) AS n FROM passages").fetchone()["n"]

    warnings = []
    if lr_have < lr_needed:
        warnings.append(
            f"Logical Reasoning: {lr_have} questions in the bank, "
            f"{lr_needed} needed for a full-length test."
        )
    if rc_have < rc_needed or passages_have < 4:
        warnings.append(
            f"Reading Comprehension: {rc_have} questions across {passages_have} "
            f"passage(s); a full-length section is {rc_needed} across 4."
        )
    if warnings:
        warnings.append(
            "This test uses reduced section sizes so that no question repeats. "
            "Timing per section still matches the real test."
        )
    return warnings
