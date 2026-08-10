# CLAUDE.md

> This file is read by Claude Code at the start of every session. It should describe
> the STABLE facts about this project — things that rarely change. For what's
> currently in progress and what's next, see `prompt.md` (read that too).

## Project Overview

- **Name:** LSAT Prep
- **Purpose:** An application to generate LSAT prep questions modeled on previous
  years' LSATs. Questions must be unique on every generation (never memorizable —
  novel logical structures, not just reworded surface text) to force real reasoning
  rather than pattern recall. Answers are graded against the correct answer key,
  with score conversion following the real LSAT raw-score-to-scaled-score (120-180)
  approach.
- **Test format (current, as of the 2024 change):** the real LSAT no longer has an
  Analytical Reasoning/Logic Games section — it was permanently removed in August 2024. The current format is two scored Logical Reasoning sections (24-26 questions
  each), one scored Reading Comprehension section (26-28 questions across 4
  passages), and one unscored experimental section, each section 35 minutes. This
  app should only ever generate Logical Reasoning and Reading Comprehension content
  — do not build or reference an Analytical Reasoning/Logic Games generator.
- **Practice modes:**
  1. **Filtered practice** — friend selects specific question types (e.g. necessary
     assumption, flaw, strengthen/weaken, parallel reasoning, inference, etc.) and/or
     RC content areas (law, science, humanities, social science), and the app
     generates/serves questions matching those filters only.
  2. **Full-length practice test** — assembles a complete test against the real
     blueprint above (2 LR sections + 1 RC section, correct question counts,
     proportional coverage of the question-type taxonomy), timed section by section.
- **Explanations must follow official LSAT methodology, not freeform LLM prose** —
  see the Explanation Methodology section below. This is a hard requirement, not a
  nice-to-have.
- **Audience:** Single friend, not a public product. No payment/billing system needed.
  Auth can stay lightweight (e.g. a single shared login or simple invite-based access)
  rather than a full multi-tenant identity system — [confirm approach before building].
- **Deployment:** Needs to be hosted somewhere the friend can access online (not
  local-only). Hosting provider/platform: [not yet decided].
- **Status:** prototype

## Versioning Strategy — READ THIS BEFORE STARTING WORK

This project is deliberately built as a series of small, numbered versions rather
than one large build, to avoid scope creep and losing track of what's done vs. in
progress.

- Each version has a **narrow, explicit scope** agreed on before work starts (see
  `prompt.md` → Version Plan).
- A version is not "started" until its scope is written down, and not "done" until
  it works end-to-end for that scope (not partially working, not "mostly done").
- Don't pull in work from a future version while implementing the current one, even
  if it seems convenient — log it in the Backlog in `prompt.md` instead and stay
  scoped.
- Example progression (adjust as needed): v0.1 = generate one Logical Reasoning
  question + grade it, no UI polish. v0.2 = add Reading Comprehension + Analytical
  Reasoning generation. v0.3 = uniqueness/dedup check via vector DB. v0.4 = scaled
  score conversion. v0.5 = deploy so friend can access it online. Etc. — refine this
  list in `prompt.md`, this is a starting shape, not a locked plan.

## Question Metadata — REQUIRED for every generated question

Every question stored in the question bank must carry these tags at creation time,
not inferred later — filtering and full-test assembly both depend on this:

- `section`: "logical_reasoning" | "reading_comprehension"
- `question_type`: one of the official LR types (necessary assumption, sufficient
  assumption, strengthen, weaken, flaw, inference/must-be-true, main point, method
  of reasoning, parallel reasoning, principle, resolve/explain, evaluate the
  argument, point at issue, role of a statement) or the relevant RC type
- `content_area` (mainly for RC passages): law, natural science, social science,
  humanities
- `difficulty` (optional, can be added later)

## Explanation Methodology — REQUIRED, do not generate freeform explanations

Explanations shown to the user must apply the **official, named LSAT reasoning
method for that question's type** — not a loose LLM paragraph that merely sounds
plausible. Since these questions are novel/AI-generated (by design, for the
uniqueness requirement), there is no real LSAT explanation to pull from — so the
substitute is rigor: the explanation must follow the same formal method a real LSAT
prep course teaches for that question type. Examples:

- **Necessary assumption questions:** explanation must apply the negation test
  explicitly — negate each candidate answer and show whether the argument falls
  apart, not just assert which one "feels" necessary.
- **Flaw questions:** the flaw must be named using the recognized taxonomy (e.g.
  causal reasoning flaw, equivocation, unrepresentative sample, ad hominem,
  circular reasoning) — not a vague "this doesn't make sense" description.
- **Sufficient assumption questions:** show the logical gap between premises and
  conclusion explicitly (e.g. via conditional logic notation), and how the correct
  answer closes it.
- **Parallel reasoning questions:** the explanation must show the abstracted
  argument structure/form being matched, not just a surface-level topic comparison.

Consider building a `.claude/skills/` entry (e.g. `lsat-methodology`) containing
the canonical method for every official question type, so it's loaded consistently
into every generation and explanation session rather than re-derived ad hoc each
time.

**Explanations are generated and verified at question-creation time, alongside the
answer key, and stored as part of the question.** Generation should use an
independent re-solve check: generate the question + answer key + methodology-based
explanation, then in a separate fresh pass (no memory of which answer was marked
correct) have the model independently apply the same named method and solve it
again. Only store the question if both passes agree. Explanations are never
generated fresh at grading time — grading stays purely deterministic (match
selected answer to stored key); the stored, pre-verified explanation is simply
displayed afterward.

## README.md — Progress Checklist

`README.md` at the repo root has a `## Progress` section listing every planned
version as a checkbox. Whenever a version is completed (fully working end-to-end
for its stated scope, not partially), check off its box in `README.md` — this is
the human-facing, at-a-glance status view, separate from the detailed log in
`prompt.md`. Keep the version list in `README.md` and the Version Plan table in
`prompt.md` in sync; if one changes, update the other.

## Reconstruction Prompts — REQUIRED AT THE END OF EVERY VERSION

When a version is completed, generate a **single, self-contained reconstruction
prompt** and add it to `prompt.md` under that version's entry. This prompt must
contain enough detail that pasting it alone into a fresh Claude Code session (empty
repo) would rebuild the project back to exactly that version's state — no other
context assumed.

A reconstruction prompt should include:

- The tech stack and key library/framework choices in use at that version.
- The project structure as of that version.
- Every feature/behavior implemented so far, described precisely enough to
  reimplement (not just "generation works" — describe what it does, its inputs/
  outputs, edge cases handled).
- Key decisions and why (pull from the Key Decisions Log in `prompt.md`).
- Explicitly note what is NOT yet implemented, so it isn't accidentally reconstructed
  ahead of scope.

Do not skip this step, even if it feels redundant with the session log — the session
log is a narrative for humans; the reconstruction prompt is a rebuild spec.

## Tech Stack

- **Language(s):** Python 3.11+ (backend), TypeScript (frontend)
- **Framework(s):**
  - Backend: FastAPI (`backend/app/main.py`) — async-friendly, good fit for
    calling the Anthropic API without blocking.
  - Frontend: Next.js 16 (App Router, TypeScript, `frontend/`) — chosen up
    front (v0.1) over a throwaway static page since a timed-test UI (v0.6)
    will need real client state anyway.
- **Database:** SQLite via Python's stdlib `sqlite3` (no ORM) — deliberately
  minimal for now; `backend/app/db.py` is a thin data-access layer designed
  to be swapped for PostgreSQL + pgvector when v0.5 (dedup) actually needs
  vector similarity search. Don't add SQLAlchemy/an ORM before that need is
  real.
- **LLM:** Anthropic API (`anthropic` Python SDK, `backend/app/generation.py`)
  — generates original Logical Reasoning questions. Gated behind
  `GENERATION_MODE=live` (see `backend/app/config.py`); defaults to
  `GENERATION_MODE=mock`, which serves hand-authored static questions from
  `backend/app/mock_questions.py` instead, so the app can be run/tested
  without spending on the API. Do not reproduce real LSAT passages/questions
  verbatim — generate original content in the same structural/logical style.
- **Package manager:** Python: `uv` (`backend/pyproject.toml` + `uv.lock`).
  Frontend: `npm` (`frontend/package.json` + `package-lock.json`).
- **Other key libraries/tools:** `pytest` (backend tests, no live-API calls
  in the suite — see `backend/tests/`), `python-dotenv` (loads
  `backend/.env`), `pydantic` (request/response models). No embedding
  model/vector store chosen yet — deferred to v0.5.

## Project Structure

Current actual structure (as of last check):

```
lsat-prep/
  .claude/
    skills/
      lsat-methodology/  - canonical LR methodology per question type,
                            explanation-rigor requirements, and a
                            target-quality reference example. Load before
                            touching backend/app/prompts.py or judging
                            generated-question quality.
    settings.json   - permissions, hooks
  backend/          - FastAPI + SQLite (stdlib sqlite3, no ORM), uv-managed
    app/
      main.py       - routes: GET /api/question/current (random LR
                       question), GET /api/passage/random (random RC
                       passage + all its questions), POST
                       /api/question/{id}/grade (deterministic key match +
                       attempts-log side effect, works for LR and RC),
                       POST /api/generate (gated behind GENERATION_MODE=
                       live), GET /api/stats/summary
      db.py         - sqlite3 connection/schema (questions, passages,
                       attempts tables)
      models.py     - Pydantic request/response models
      config.py     - env loading (ANTHROPIC_API_KEY, GENERATION_MODE, DB_PATH)
      generation.py - live generate -> independent re-solve -> retry pipeline
      prompts.py    - system prompts (methodology reference, rigor
                       requirements, target-quality example)
      mock_questions.py - hand-authored static LR questions for GENERATION_MODE=mock
      rc_content.py - hand-authored RC passages + questions (same
                       verification method as LR)
    scripts/
      generate_question.py - seeding CLI (mock or live), seeds LR + RC
      export_prep_txt.py   - regenerates prep.txt from mock_questions.py +
                       rc_content.py (run after authoring any new question)
    tests/          - pytest: test_grading.py, test_stats.py,
                       test_reading_comp.py (no live API calls)
    data/           - sqlite file (gitignored)
  frontend/         - Next.js 16 (App Router, TypeScript), npm-managed
    app/
      layout.tsx    - root layout, fonts (Geist + Press Start 2P + Fredoka), nav bar
      globals.css   - theme tokens (light/dark), wood-panel/block-btn/
                       dashboard component styles
      page.tsx      - LR practice page: view question, submit, see grade +
                       explanation (clean-card reading area, themed chrome)
      reading-comp/page.tsx - RC practice page: passage pinned in a
                       clean-card while cycling through its questions in
                       sequence, then a new random passage
      progress/page.tsx - /progress dashboard: overall accuracy, accuracy
                       by type, attempts over time
  .gitignore
  .claudeignore
  CLAUDE.md
  prompt.md
  README.md
  prep.txt          - derived export of the full question bank (LR + RC),
                       regenerated by scripts/export_prep_txt.py - never
                       hand-edit
```

[Update this section whenever the structure changes — keep it accurate, not aspirational.]

## Coding Conventions

- **Naming:** snake_case for Python (files, functions, variables), camelCase
  for TypeScript variables/functions, PascalCase for React components/types.
- **Error handling:** Python: FastAPI's `HTTPException` raised directly from
  route handlers (see `backend/app/main.py`) — no custom exception hierarchy
  yet, that's premature at this scale. A dedicated `GenerationError` exists
  in `backend/app/generation.py` for the generate/verify pipeline. TypeScript:
  plain thrown `Error`s caught in the component and surfaced via `useState`
  (see `frontend/app/page.tsx`, `frontend/app/progress/page.tsx`) — no
  Result-style wrapper.
- **Formatting/linting:** not yet configured for either side (no ruff/black,
  no ESLint config beyond Next.js's default). Add if/when it starts to bite.
- **Testing:** `pytest` for backend (`backend/tests/`), one file per concern
  (`test_grading.py`, `test_stats.py`) rather than one per module. Tests use
  a temp SQLite DB per test via `tmp_path` + `monkeypatch` — never touch the
  real `backend/data/` DB. No live Anthropic API calls in tests (see
  Workflow Notes). No frontend test suite yet.
- **Comments/docs style:** minimal — comments only where the *why* isn't
  obvious from the code (see e.g. the `explanation_viewed` note in
  `main.py`'s grade route). No docstrings-by-default convention.
- **Other conventions:** CSS theme values are CSS custom properties
  (`frontend/app/globals.css`), not hardcoded hex in components — this is
  what let the v0.9 Growtopia theme reskin v0.4's dashboard by swapping
  token values only. Any new chart/dashboard UI should load the `dataviz`
  skill first and run its `validate_palette.js` on any new color choices
  rather than eyeballing contrast/CVD-safety.

## Commands

- **Install deps (backend):** `cd backend && uv sync`
- **Install deps (frontend):** `cd frontend && npm install`
- **Run dev server (backend):** `cd backend && uv run uvicorn app.main:app --reload --port 8000`
- **Run dev server (frontend):** `cd frontend && npm run dev` (expects
  `NEXT_PUBLIC_API_URL` in `frontend/.env.local`, defaults to
  `http://localhost:8000`)
- **Seed/generate a question:** `cd backend && uv run python scripts/generate_question.py`
  (mock or live, per `GENERATION_MODE` in `backend/.env`)
- **Export the study file:** `cd backend && uv run python scripts/export_prep_txt.py`
  (regenerates `prep.txt` at the repo root from `mock_questions.py` +
  `rc_content.py` — see Workflow Notes, run this after authoring any new
  question)
- **Run tests:** `cd backend && uv run pytest`
- **Lint:** not configured yet.
- **Build (frontend):** `cd frontend && npm run build` — run and passing as of
  v0.2 (Next.js 16 / Turbopack; all 4 routes prerender static: `/`,
  `/progress`, `/reading-comp`, `/_not-found`). `npx tsc --noEmit` also passes
  clean. No backend build step (interpreted, no packaging target).
- **Deploy:** not yet decided — see Project Overview → Deployment.

## Do NOT touch / modify without asking

- `backend/.env` and `frontend/.env.local` — never commit real secrets; both
  are gitignored. `backend/.env.example` is the template and IS meant to be
  committed, but only with placeholder values.
- `backend/data/` — the local SQLite runtime data file; gitignored, don't
  commit it or hand-edit it outside the app's own code paths.
- `frontend/AGENTS.md` and `frontend/CLAUDE.md` — auto-generated/rewritten by
  `next dev` itself (Next.js version-specific agent notes); don't hand-edit,
  they regenerate on their own.
- `.claude/skills/lsat-methodology/SKILL.md` — keep in sync with
  `backend/app/prompts.py` if either changes; don't let them drift (see that
  skill file's own note on this).
- `prep.txt` (repo root) — a derived export of `app/mock_questions.py` +
  `app/rc_content.py`, regenerated by `scripts/export_prep_txt.py`. Never
  hand-edit; add/change questions in the source files and re-run the script.

## PR / Commit Conventions

- **Commit message format:** plain, descriptive messages — no strict
  Conventional Commits prefix enforced. Version-completion commits name the
  version and summarize what it added (e.g. `v0.3: filtered practice mode +
  question metadata tagging`); interim/checkpoint commits are labeled as such.
- **Branch naming:** single `main` branch so far — no feature-branch workflow
  in use yet at this project's current (single-developer-session) stage.
- **Tags:** annotated tags (`git tag -a vX.Y -m "..."`) mark completed-version
  commits only — see Workflow Notes → Finishing a Version checklist. Don't
  tag work-in-progress commits.
- **Pushing:** never commit/tag/push without first showing the user what
  would be pushed and getting their explicit confirmation — see Workflow
  Notes.

## Workflow Notes

- Read `prompt.md` at the start of every session for current project state, active
  tasks, version plan, and recent decisions.
- Stay inside the current version's scope (see Versioning Strategy above) — log
  anything out-of-scope to the Backlog in `prompt.md` instead of building it now.
- Use Plan Mode for any non-trivial or multi-file change — review the plan before
  accepting.
- Run tests/lint after any change before considering it done.
- Never generate or store verbatim real LSAT questions/passages — generation must
  produce original content inspired by structure and style only.
- Every newly generated question must pass the uniqueness/similarity check before
  being served to the user — no exceptions, even in dev/testing shortcuts.
- **Whenever a new question (LR or RC) is authored and verified**, add it to
  `app/mock_questions.py` or `app/rc_content.py` (the canonical source) —
  including its `explanation` field, which must contain the full
  methodology-based reasoning for why the correct answer is correct (per
  the Explanation Methodology section above), not just the answer letter —
  then regenerate `prep.txt` at the repo root:
  `cd backend && uv run python scripts/export_prep_txt.py`. The export
  script pulls `correct_answer` and `explanation` straight from the source
  data, so every `prep.txt` entry automatically includes the reasoning as
  long as the source question does. Never hand-edit `prep.txt` directly —
  it's a derived export and gets overwritten.
- **Finishing a version — REQUIRED CHECKLIST.** Run this only when a version is
  genuinely, fully complete end-to-end for its stated scope, per the Versioning
  Strategy rules above — never for work-in-progress or partially-complete states.
  If you're unsure whether a version counts as complete, ask before running this
  checklist or pushing anything — do not guess.
  1. Update `prompt.md`: the Current State section, that version's status in the
     Version Plan table, and a Session Log entry for the work.
  2. Check off that version's box in `README.md`'s Progress checklist.
  3. Write the required reconstruction prompt (per the Reconstruction Prompts
     section above) into that version's Session Log entry in `prompt.md`, and add
     a row for it to the Reconstruction Prompts Index table.
  4. Present the user a checklist summarizing steps 1-3 and the code changes that
     make up the version, and **stop for their explicit confirmation that
     everything is correct** — do not commit, tag, or push until they confirm.
  5. Once confirmed: commit everything from steps 1-3 together with the actual
     code changes for that version, in a commit message that names the version
     and summarizes what it added (e.g.
     `v0.3: filtered practice mode + question metadata tagging`).
  6. Tag the commit as an **annotated tag using the version name as the tag's
     note/message** (e.g. `git tag -a v0.3 -m "v0.3: filtered practice mode +
     question metadata tagging"`) — a fast way to check out that exact point in
     history later, separate from and complementary to the reconstruction prompt.
  7. Push both the commit and the tag to GitHub: `git push && git push --tags`.
- [add any other standing instructions you want Claude to always follow]
