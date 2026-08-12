import json

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app import assembly, scoring
from app.config import GENERATION_MODE
from app.db import (
    get_attempts_by_day,
    get_connection,
    get_overall_stats,
    get_question_by_id,
    get_questions_by_passage_id,
    get_questions_filtered,
    get_random_passage,
    get_random_question,
    get_stats_by_type,
    get_taxonomy_counts,
    insert_attempt,
    insert_question,
)
from app.generation import GenerationError, generate_and_verify
from app.models import (
    VALID_ANSWERS,
    ContentAreaCount,
    DayStats,
    FilteredQuestions,
    GradeRequest,
    GradeResponse,
    OverallStats,
    PassagePublic,
    PassageWithQuestions,
    QuestionPublic,
    StatsSummary,
    Taxonomy,
    TestGradeRequest,
    TestGradeResponse,
    TestPaper,
    TestQuestionResult,
    TestSection,
    TypeCount,
    TypeStats,
)

app = FastAPI(title="LSAT Prep API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _row_to_public(row) -> QuestionPublic:
    return QuestionPublic(
        id=row["id"],
        section=row["section"],
        question_type=row["question_type"],
        content_area=row["content_area"],
        passage_id=row["passage_id"],
        stimulus=row["stimulus"],
        question_stem=row["question_stem"],
        choices=json.loads(row["choices"]),
    )


@app.get("/api/question/current", response_model=QuestionPublic)
def get_current_question():
    """Returns a random question from the bank on every call, so repeated
    requests (e.g. the frontend's Reload button) cycle through different
    questions instead of always re-serving the same one."""
    with get_connection() as conn:
        row = get_random_question(conn)
    if row is None:
        raise HTTPException(status_code=404, detail="No question has been generated yet")
    return _row_to_public(row)


@app.get("/api/passage/random", response_model=PassageWithQuestions)
def get_random_passage_with_questions():
    """Reading Comprehension flow: a passage is read once, then its
    questions are answered in sequence — unlike LR's per-question random
    draw, this returns one random passage plus ALL of its questions
    together so the frontend can keep the passage pinned while cycling
    through them."""
    with get_connection() as conn:
        passage_row = get_random_passage(conn)
        if passage_row is None:
            raise HTTPException(status_code=404, detail="No passages have been added yet")
        question_rows = get_questions_by_passage_id(conn, passage_row["id"])

    return PassageWithQuestions(
        passage=PassagePublic(
            id=passage_row["id"],
            content_area=passage_row["content_area"],
            title=passage_row["title"],
            passage_text=passage_row["passage_text"],
        ),
        questions=[_row_to_public(row) for row in question_rows],
    )


@app.get("/api/taxonomy", response_model=Taxonomy)
def get_taxonomy():
    """Question types and content areas actually present in the bank, with
    counts. The /focus page builds its filter controls from this rather than a
    hardcoded list, so the options can't drift as content is added."""
    with get_connection() as conn:
        type_rows, area_rows = get_taxonomy_counts(conn)

    return Taxonomy(
        types=[
            TypeCount(
                section=row["section"],
                question_type=row["question_type"],
                count=row["count"],
            )
            for row in type_rows
        ],
        content_areas=[
            ContentAreaCount(content_area=row["content_area"], count=row["count"])
            for row in area_rows
        ],
    )


@app.get("/api/questions/filtered", response_model=FilteredQuestions)
def get_filtered_questions(
    section: str | None = Query(None),
    question_type: list[str] | None = Query(None),
    content_area: list[str] | None = Query(None),
):
    """Filtered practice: returns the ENTIRE matching set at once, in random
    order, so the frontend can cycle through it without repeats — the same
    shape as the RC flow, rather than LR's one-random-question-per-call draw.

    A filter combination that matches nothing is a valid answer, not an error:
    this returns 200 with total=0 so the page can say "no questions match"
    instead of surfacing a failure."""
    with get_connection() as conn:
        rows = get_questions_filtered(
            conn,
            section=section,
            question_types=question_type,
            content_areas=content_area,
        )

    questions = [_row_to_public(row) for row in rows]
    return FilteredQuestions(total=len(questions), questions=questions)


@app.get("/api/test/new", response_model=TestPaper)
def new_test(preset: str = Query(assembly.DEFAULT_PRESET)):
    """Assemble a full-length timed practice test.

    No question appears twice anywhere in the paper. Returns 400 with a
    countable message when the bank can't fill the requested preset — that is
    how "blueprint" stays honest instead of silently serving a half-test."""
    with get_connection() as conn:
        try:
            paper = assembly.assemble_test(conn, preset)
        except assembly.AssemblyError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        warnings = assembly.content_warnings(conn)

    return TestPaper(
        preset=paper["preset"],
        warnings=warnings,
        sections=[
            TestSection(
                kind=section["kind"],
                label=section["label"],
                minutes=section["minutes"],
                passages=[
                    PassagePublic(
                        id=row["id"],
                        content_area=row["content_area"],
                        title=row["title"],
                        passage_text=row["passage_text"],
                    )
                    for row in section["passages"]
                ],
                questions=[_row_to_public(row) for row in section["questions"]],
            )
            for section in paper["sections"]
        ],
    )


@app.post("/api/test/grade", response_model=TestGradeResponse)
def grade_test(body: TestGradeRequest):
    """Grade a whole test at once.

    Same deterministic key match as single-question grading, and it still logs
    an attempt per ANSWERED question so a test feeds /progress exactly like
    ordinary practice. A blank answer is scored incorrect and logs nothing —
    the real LSAT has no guessing penalty, but a blank is still wrong, and
    recording a non-attempt would distort accuracy-by-type."""
    results: list[TestQuestionResult] = []
    correct_count = 0
    answered_count = 0

    with get_connection() as conn:
        for answer in body.answers:
            row = get_question_by_id(conn, answer.question_id)
            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Question not found: {answer.question_id}",
                )
            if answer.selected_answer is not None and (
                answer.selected_answer not in VALID_ANSWERS
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"selected_answer must be one of {VALID_ANSWERS} or null",
                )

            correct = answer.selected_answer == row["correct_answer"]
            if correct:
                correct_count += 1
            if answer.selected_answer is not None:
                answered_count += 1
                insert_attempt(
                    conn,
                    question_id=answer.question_id,
                    selected_answer=answer.selected_answer,
                    correct=correct,
                    explanation_viewed=True,
                )

            results.append(
                TestQuestionResult(
                    question_id=answer.question_id,
                    selected_answer=answer.selected_answer,
                    correct=correct,
                    correct_answer=row["correct_answer"],
                    explanation=row["explanation"],
                )
            )

    total = len(body.answers)
    scaled = scoring.scaled_score(correct_count, total)

    return TestGradeResponse(
        total=total,
        correct=correct_count,
        answered=answered_count,
        scaled_score=scaled,
        percentile=scoring.percentile_band(scaled) if scaled is not None else None,
        scaled_is_estimated=scoring.is_estimated(total),
        results=results,
    )


@app.post("/api/question/{question_id}/grade", response_model=GradeResponse)
def grade_question(question_id: int, body: GradeRequest):
    if body.selected_answer not in VALID_ANSWERS:
        raise HTTPException(
            status_code=400, detail=f"selected_answer must be one of {VALID_ANSWERS}"
        )
    with get_connection() as conn:
        row = get_question_by_id(conn, question_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Question not found")

        # Grading is a pure deterministic key-match, computed before anything
        # below is touched. The attempts-log insert that follows is a side
        # effect for the /progress dashboard only - it is never read back to
        # influence this comparison. explanation_viewed=True because this UI
        # shows the explanation as part of this same response (grading and
        # explanation display are one atomic action here, not a separate
        # reveal step).
        correct = body.selected_answer == row["correct_answer"]
        insert_attempt(
            conn,
            question_id=question_id,
            selected_answer=body.selected_answer,
            correct=correct,
            explanation_viewed=True,
        )

    return GradeResponse(
        correct=correct,
        correct_answer=row["correct_answer"],
        explanation=row["explanation"],
    )


@app.get("/api/stats/summary", response_model=StatsSummary)
def get_stats_summary():
    with get_connection() as conn:
        overall_row = get_overall_stats(conn)
        by_type_rows = get_stats_by_type(conn)
        over_time_rows = get_attempts_by_day(conn)

    total = overall_row["total"]
    correct = overall_row["correct"]
    overall = OverallStats(
        total=total,
        correct=correct,
        accuracy=(correct / total) if total > 0 else None,
    )
    by_type = [
        TypeStats(
            question_type=row["question_type"],
            total=row["total"],
            correct=row["correct"],
            accuracy=row["correct"] / row["total"],
        )
        for row in by_type_rows
    ]
    over_time = [
        DayStats(date=row["date"], count=row["count"]) for row in over_time_rows
    ]
    return StatsSummary(overall=overall, by_type=by_type, over_time=over_time)


@app.post("/api/generate", response_model=QuestionPublic)
def generate():
    if GENERATION_MODE != "live":
        raise HTTPException(
            status_code=400,
            detail=(
                "Live generation is disabled while GENERATION_MODE=mock. "
                "Run scripts/generate_question.py to reseed mock questions, "
                "or set GENERATION_MODE=live (with ANTHROPIC_API_KEY set) to "
                "enable live generation."
            ),
        )
    try:
        question = generate_and_verify()
    except GenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    with get_connection() as conn:
        question_id = insert_question(conn, question)
        row = get_question_by_id(conn, question_id)
    return _row_to_public(row)
