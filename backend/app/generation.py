import json

from anthropic import Anthropic

from app.config import ANTHROPIC_API_KEY
from app.models import VALID_ANSWERS
from app.prompts import (
    GENERATION_SYSTEM_PROMPT,
    VERIFY_SYSTEM_PROMPT,
    build_verify_user_message,
)

MODEL = "claude-sonnet-5"
MAX_GENERATE_VERIFY_ATTEMPTS = 3
MAX_JSON_PARSE_RETRIES = 1

REQUIRED_GENERATION_KEYS = {
    "question_type",
    "stimulus",
    "question_stem",
    "choices",
    "correct_answer",
    "explanation",
}


class GenerationError(Exception):
    pass


def _client() -> Anthropic:
    if not ANTHROPIC_API_KEY:
        raise GenerationError(
            "ANTHROPIC_API_KEY is not set. Add it to backend/.env before generating."
        )
    return Anthropic(api_key=ANTHROPIC_API_KEY)


def _call_and_parse_json(client: Anthropic, system: str, user_message: str) -> dict:
    last_error = None
    for _ in range(MAX_JSON_PARSE_RETRIES + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=system,
            messages=[{"role": "user", "content": user_message}],
        )
        raw_text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            last_error = exc
            user_message = (
                f"{user_message}\n\nYour previous response was not valid JSON "
                f"({exc}). Respond again with ONLY the JSON object, no other text."
            )
    raise GenerationError(f"Model did not return valid JSON: {last_error}")


def generate_question(client: Anthropic) -> dict:
    data = _call_and_parse_json(
        client,
        GENERATION_SYSTEM_PROMPT,
        "Generate one original LSAT Logical Reasoning question now.",
    )

    missing = REQUIRED_GENERATION_KEYS - data.keys()
    if missing:
        raise GenerationError(f"Generated question missing keys: {missing}")
    if len(data["choices"]) != 5:
        raise GenerationError("Generated question must have exactly 5 choices")
    if data["correct_answer"] not in VALID_ANSWERS:
        raise GenerationError(
            f"correct_answer must be one of {VALID_ANSWERS}, got {data['correct_answer']!r}"
        )
    return data


def verify_question(client: Anthropic, question: dict) -> dict:
    data = _call_and_parse_json(
        client,
        VERIFY_SYSTEM_PROMPT,
        build_verify_user_message(question),
    )
    if "chosen_answer" not in data or "explanation" not in data:
        raise GenerationError("Verification response missing required keys")
    if data["chosen_answer"] not in VALID_ANSWERS:
        raise GenerationError(
            f"chosen_answer must be one of {VALID_ANSWERS}, got {data['chosen_answer']!r}"
        )
    return data


def generate_and_verify() -> dict:
    """Generate a question, independently re-solve it, and only return it if
    the independent pass agrees with the generation pass's answer key.
    Retries from scratch (fresh generation) on mismatch, up to
    MAX_GENERATE_VERIFY_ATTEMPTS times.
    """
    client = _client()
    last_mismatch = None

    for attempt in range(1, MAX_GENERATE_VERIFY_ATTEMPTS + 1):
        generated = generate_question(client)
        verification = verify_question(client, generated)

        if verification["chosen_answer"] == generated["correct_answer"]:
            return {
                "section": "logical_reasoning",
                "question_type": generated["question_type"],
                "content_area": None,
                "stimulus": generated["stimulus"],
                "question_stem": generated["question_stem"],
                "choices": generated["choices"],
                "correct_answer": generated["correct_answer"],
                "explanation": generated["explanation"],
                "verified": True,
            }

        last_mismatch = {
            "attempt": attempt,
            "generated_answer": generated["correct_answer"],
            "verification_answer": verification["chosen_answer"],
        }

    raise GenerationError(
        f"Independent re-solve did not match generated answer after "
        f"{MAX_GENERATE_VERIFY_ATTEMPTS} attempts. Last mismatch: {last_mismatch}"
    )
