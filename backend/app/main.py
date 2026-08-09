import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import GENERATION_MODE
from app.db import (
    get_attempts_by_day,
    get_connection,
    get_latest_question,
    get_overall_stats,
    get_question_by_id,
    get_stats_by_type,
    insert_attempt,
    insert_question,
)
from app.generation import GenerationError, generate_and_verify
from app.models import (
    VALID_ANSWERS,
    DayStats,
    GradeRequest,
    GradeResponse,
    OverallStats,
    QuestionPublic,
    StatsSummary,
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
        stimulus=row["stimulus"],
        question_stem=row["question_stem"],
        choices=json.loads(row["choices"]),
    )


@app.get("/api/question/current", response_model=QuestionPublic)
def get_current_question():
    with get_connection() as conn:
        row = get_latest_question(conn)
    if row is None:
        raise HTTPException(status_code=404, detail="No question has been generated yet")
    return _row_to_public(row)


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
