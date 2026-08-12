from pydantic import BaseModel

VALID_ANSWERS = ("A", "B", "C", "D", "E")


class QuestionPublic(BaseModel):
    id: int
    section: str
    question_type: str
    content_area: str | None
    passage_id: int | None
    stimulus: str | None  # null for RC questions - text lives on the passage
    question_stem: str
    choices: list[str]


class PassagePublic(BaseModel):
    id: int
    content_area: str
    title: str | None
    passage_text: str


class PassageWithQuestions(BaseModel):
    passage: PassagePublic
    questions: list[QuestionPublic]


class TypeCount(BaseModel):
    section: str
    question_type: str
    count: int


class ContentAreaCount(BaseModel):
    content_area: str
    count: int


class Taxonomy(BaseModel):
    types: list[TypeCount]
    content_areas: list[ContentAreaCount]


class FilteredQuestions(BaseModel):
    total: int
    questions: list[QuestionPublic]


class TestSection(BaseModel):
    kind: str
    label: str
    minutes: int
    passages: list[PassagePublic]
    questions: list[QuestionPublic]


class TestPaper(BaseModel):
    preset: str
    sections: list[TestSection]
    # Where the bank falls short of a real blueprint, stated plainly so the UI
    # never implies the test is full-length.
    warnings: list[str]


class TestAnswer(BaseModel):
    question_id: int
    selected_answer: str | None  # null = left blank, scored incorrect


class TestGradeRequest(BaseModel):
    answers: list[TestAnswer]


class TestQuestionResult(BaseModel):
    question_id: int
    selected_answer: str | None
    correct: bool
    correct_answer: str
    explanation: str


class TestGradeResponse(BaseModel):
    total: int
    correct: int
    answered: int
    results: list[TestQuestionResult]


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
