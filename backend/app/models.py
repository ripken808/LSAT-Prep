from pydantic import BaseModel

VALID_ANSWERS = ("A", "B", "C", "D", "E")


class QuestionPublic(BaseModel):
    id: int
    section: str
    question_type: str
    content_area: str | None
    stimulus: str
    question_stem: str
    choices: list[str]


class GradeRequest(BaseModel):
    selected_answer: str


class GradeResponse(BaseModel):
    correct: bool
    correct_answer: str
    explanation: str


class OverallStats(BaseModel):
    total: int
    correct: int
    accuracy: float | None  # None when total == 0 (no attempts yet)


class TypeStats(BaseModel):
    question_type: str
    total: int
    correct: int
    accuracy: float


class DayStats(BaseModel):
    date: str
    count: int


class StatsSummary(BaseModel):
    overall: OverallStats
    by_type: list[TypeStats]
    over_time: list[DayStats]
