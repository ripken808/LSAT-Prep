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

- **Language(s):** Python (backend), TypeScript (frontend)
- **Framework(s):**
  - Backend: [FastAPI recommended — async-friendly, good fit for calling the Claude
    API and running similarity checks without blocking]
  - Frontend: [Next.js (React) recommended — needed for a timed-test UI]
- **Database:** [PostgreSQL recommended, e.g. via SQLAlchemy/SQLModel] + [pgvector
  extension or a dedicated vector store for the uniqueness/similarity check]
- **LLM:** Claude API — generates original questions per LSAT section type (Logical
  Reasoning, Analytical Reasoning, Reading Comprehension). Do not reproduce real
  LSAT passages/questions verbatim — generate original content in the same
  structural/logical style.
- **Package manager:** [Python: poetry or uv — pick one] / [Frontend: pnpm or npm]
- **Other key libraries/tools:** [e.g. embedding model or library for similarity
  checks, testing framework, anything version-sensitive Claude should know about]

## Project Structure

Current actual structure (as of last check):

```
lsat-prep/
  .claude/
    skills/         - [list/describe skills as they're added]
    settings.json   - permissions, hooks
  src/              - [contents not yet documented — update this once src/ is
                        populated; likely needs backend/ and frontend/ subfolders
                        or a top-level split, decide and record here]
  .claudeignore
  CLAUDE.md
  prompt.md
```

[Update this section whenever the structure changes — keep it accurate, not aspirational.]

## Coding Conventions

- **Naming:** [e.g. snake_case for Python, camelCase for TypeScript/React]
- **Error handling:** [e.g. Python: custom exception classes + FastAPI exception
  handlers / TypeScript: Result-style or thrown errors — decide and note here]
- **Formatting/linting:** [e.g. Python: ruff + black / Frontend: ESLint + Prettier]
- **Testing:** [e.g. pytest for backend, Vitest for frontend — one test file per
  module, aim for X% coverage]
- **Comments/docs style:** [e.g. docstrings on public functions only]
- **Other conventions:** [anything specific to how you write code here]

## Commands

- **Install deps (backend):** `[command]`
- **Install deps (frontend):** `[command]`
- **Run dev server (backend):** `[command]`
- **Run dev server (frontend):** `[command]`
- **Run tests:** `[command]`
- **Lint:** `[command]`
- **Build:** `[command]`
- **Deploy:** `[command, once hosting platform is decided]`

## Do NOT touch / modify without asking

- [e.g. `db/migrations/` — write new migrations, never edit existing ones]
- [e.g. `.env.example` — update but never commit real secrets or API keys]
- [anything auto-generated, vendored, or fragile]

## PR / Commit Conventions

- **Commit message format:** [e.g. Conventional Commits — feat:, fix:, chore:]
- **Branch naming:** [e.g. feature/xxx, fix/xxx]
- **PR description should include:** [e.g. summary, testing notes, risk/rollback plan]

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
- At the end of every completed version, write a Reconstruction Prompt into
  `prompt.md` per the Reconstruction Prompts section above — this is required, not
  optional.
- At the end of every completed version, also check off that version's box in
  `README.md` — do this alongside the reconstruction prompt, not instead of it.
- [add any other standing instructions you want Claude to always follow]
