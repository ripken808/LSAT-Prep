import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
DB_PATH = BACKEND_DIR / "data" / "lsat_prep.db"

# "mock" (default) serves the hand-authored static questions in
# app/mock_questions.py - no API key or network calls required.
# "live" calls the real generate_and_verify() pipeline against the
# Anthropic API. Switch by setting GENERATION_MODE=live in backend/.env.
GENERATION_MODE = os.environ.get("GENERATION_MODE", "mock")
