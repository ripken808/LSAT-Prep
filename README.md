# LSAT Prep

An app that generates unique LSAT practice questions modeled on previous years'
LSATs — never memorizable, always original — and grades answers against real LSAT
grading conventions.

Built for a friend, not a public product. See `CLAUDE.md` for engineering
conventions and `prompt.md` for the detailed session-by-session log.

---

## Progress

> Claude Code: check off a box here when that version is fully working end-to-end
> for its stated scope — not partially working. Update this alongside `prompt.md`
> (Version Plan table + Session Log) and the required reconstruction prompt. Don't
> check a box off early to look further along than the project actually is.
>
> **Version numbers are scope IDs, not build order.** Actual completion order so
> far: v0.4 → v0.9 → v0.1 → v0.2 (four done). See the Build order column in
> `prompt.md`'s Version Plan for the full record and why the numbers were not
> renumbered.

- [x] **v0.1** — Hand-authored, independently-verified Logical Reasoning
      question bank (14 questions, all 14 official LR types) + verified answer
      key + methodology-based explanation, serve a random question and grade
      a user's answer. No live Anthropic API required (revised scope).
- [x] **v0.2** — Reading Comprehension: hand-authored, independently-verified
      passages + questions (2 passages to start — law, natural science; more
      content areas backlogged). No Analytical Reasoning — not part of the
      current real LSAT.
- [ ] **v0.3** — Question metadata tagging + filtered practice mode (pick question
      types / content areas to practice).
- [x] **v0.4** — Practice stats dashboard (attempts history + `/progress` page:
      overall accuracy, accuracy by type, attempts over time). No streaks/XP/badges.
- [ ] **v0.5** — Uniqueness/dedup check via vector DB.
- [ ] **v0.6** — Full-length practice test assembly (real blueprint, timed sections).
- [ ] **v0.7** — Scaled score conversion (120-180).
- [ ] **v0.8** — Deploy so friend can access it online.
- [x] **v0.9** — Growtopia-inspired visual theme (cosmetic/CSS-only; original
      pixel-chunky UI, question-reading screen stays clean/unstyled).
- [ ] v0.x — [add more as scope becomes clearer]

---

## Getting Started

```bash
# backend
cd backend
uv sync
cp .env.example .env   # defaults to GENERATION_MODE=mock, no API key needed
uv run python scripts/generate_question.py   # seeds mock questions
uv run uvicorn app.main:app --reload --port 8000

# frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000` (LR practice), `http://localhost:3000/reading-comp`
(RC practice), and `http://localhost:3000/progress` (stats dashboard). To use real
Anthropic-API-generated LR questions instead of the hand-authored set, set
`GENERATION_MODE=live` and a real `ANTHROPIC_API_KEY` in `backend/.env`, then
re-run the seeding script.

The full question bank (LR + RC, with answers and explanations) is also available
as plain text in `prep.txt` at the repo root — regenerate it with
`uv run python scripts/export_prep_txt.py` after adding any new question.

See `CLAUDE.md` → Commands for the full command reference (tests, etc.).

## Tech Stack

See `CLAUDE.md` → Tech Stack for the full, current breakdown.

## License

[Not applicable / personal project — add if this ever becomes shareable beyond one friend]
