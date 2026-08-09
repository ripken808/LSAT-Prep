# Project Log — LSAT Prep

> Working memory that survives context compaction and new sessions. @-mention this
> file at the start of every Claude Code session. Update it at the END of every
> session, before closing out. See `CLAUDE.md` for stable project conventions,
> versioning strategy, and the reconstruction prompt requirement.

---

## Current State (overwrite this section each time — don't append)

- **Current version:** v0.1 — in progress, NOT complete
- **Status:** Full generate→verify→grade app is built and working end-to-end,
  but currently running in `GENERATION_MODE=mock` (see `backend/app/config.py`)
  to avoid Anthropic API spend during testing. Mock mode serves 3
  hand-authored static questions from `backend/app/mock_questions.py` — no
  live API calls happen in this mode. **v0.1's actual goal — proving the live
  generate→verify pipeline (real Anthropic API calls, independent re-solve
  check, retry-on-mismatch) works end-to-end — has NOT yet been demonstrated.**
  The live pipeline code exists and is untouched/unsimplified
  (`backend/app/generation.py`, `backend/app/prompts.py`) but has never
  actually been run against the real API. Do not check off v0.1 in
  `README.md` or write its reconstruction prompt until `GENERATION_MODE=live`
  has been run for real and verified end-to-end in the browser.
- **Also this session (explicitly authorized out-of-sequence, since v0.1 is
  blocked on an external dependency — see Blockers):** built v0.4 (attempts
  table + `/progress` stats dashboard) and v0.9 (Growtopia-inspired visual
  theme) end to end. Backend for both is fully covered by passing pytest
  (13 tests total) and curl-verified real data flow. **Frontend for both has
  NOT been visually confirmed in an actual rendered browser** — this
  environment has no working headless browser (chromium cask present but
  the `.app` binary is missing), so verification stopped at: compiles with
  no errors, correct classes/CSS-variable tokens present in server-rendered
  HTML, and the Growtopia-theme palette contrast-validated with the dataviz
  skill's validator script. Per CLAUDE.md's UI-testing convention, this is
  disclosed rather than claimed as verified — **do not check off v0.4 or
  v0.9 in `README.md` until a real browser check confirms they render
  correctly.** Both dev servers are running (backend :8000, frontend :3000)
  for that check.
- **Repo status:** Everything above is pushed to GitHub
  (`github.com/ripken808/LSAT-Prep`, branch `main`) as a plain checkpoint
  commit (`96dbc78`, no version tag — nothing has cleared the "genuinely
  complete" bar yet, so no version tag was applied, per explicit user
  instruction). `CLAUDE.md` now encodes the full finishing-a-version
  checklist (update docs → checklist for user confirmation → commit → tag →
  push) in its Workflow Notes — see Session 3 below. The user's standing
  preference (confirm before any commit/tag/push, annotated tags with the
  version name as the note) is also saved to Claude's cross-session memory,
  not just this repo's `CLAUDE.md`.
- **Last touched file(s) (docs-only sync pass):** `CLAUDE.md` (Tech Stack,
  Commands, Coding Conventions, Do NOT touch, PR/Commit Conventions,
  Project Structure all filled in with concrete current values),
  `README.md` (Getting Started filled in), `prompt.md` (this file).
- **Branch:** main
- **Blockers:**
  1. Need an `ANTHROPIC_API_KEY` from the user to switch to
     `GENERATION_MODE=live` and complete v0.1 for real.
  2. Need the user (or a working browser in-session) to visually confirm
     v0.4's dashboard and v0.9's theme actually render as intended before
     either is checked off.

---

## Version Plan

> Small, explicitly-scoped versions — see Versioning Strategy in CLAUDE.md. Don't
> start a version until its scope is written here. Mark complete only when it works
> end-to-end for its stated scope.

| Version | Scope                                                                                                                                                                                                                                                                  | Status          |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| v0.1    | Generate one Logical Reasoning question + answer key + methodology-based explanation (with independent re-solve verification), grade a single user answer against it. No dedup check yet, no UI polish, no filtering. Prove the core generate-verify-grade loop works. | [~] in progress — app built, running in mock mode; live pipeline not yet run/verified |
| v0.2    | Add Reading Comprehension generation (passage + questions). No Analytical Reasoning — it's not part of the current real LSAT (removed Aug 2024).                                                                                                                       | [ ] not started |
| v0.3    | Question metadata tagging (section, question_type, content_area) + filtered practice mode (select types/content areas to practice)                                                                                                                                     | [ ] not started |
| v0.4    | Practice stats dashboard (Gamification Concept 1 only — no streaks/XP/badges): `attempts` table (question_id, selected_answer, correct, explanation_viewed, answered_at) written by the grading endpoint as a pure side effect — grading logic itself does not change, zero read dependency on this data. `/progress` page (own nav link, never shown during a question): overall accuracy, accuracy by question type, attempts over time. | [~] built, backend fully tested (9 passing pytest); frontend compiles/serves real data but not yet visually confirmed in a browser |
| v0.5    | Uniqueness/dedup check via vector DB                                                                                                                                                                                                                                   | [ ] not started |
| v0.6    | Full-length practice test assembly (real blueprint: 2 LR + 1 RC, correct question counts, timed sections)                                                                                                                                                              | [ ] not started |
| v0.7    | Scaled score conversion (120-180)                                                                                                                                                                                                                                      | [ ] not started |
| v0.8    | Deploy so friend can access it online                                                                                                                                                                                                                                  | [ ] not started |
| v0.9    | Growtopia-inspired visual theme (cosmetic/CSS-only — no grading/generation/data-model changes). Original pixel-chunky UI: wood-panel borders/textures, beveled 3D block buttons, bright saturated palette, applied to nav, buttons, general chrome, and the themed `/progress` dashboard. Press Start 2P reserved for headings/large stat numbers only; a legible rounded sans font for nav links, button labels, and badge text. The question-reading screen (stimulus/stem/choices) stays clean, high-contrast, unstyled by the pixel theme. | [~] built, palette contrast-validated + compiles clean; not yet visually confirmed in a browser |
| v0.x    | [add more as scope becomes clearer]                                                                                                                                                                                                                                    | [ ] not started |

---

## Next Up (current version's immediate tasks)

- [ ] Get ANTHROPIC_API_KEY from user, set GENERATION_MODE=live in backend/.env
- [ ] Run scripts/generate_question.py in live mode, sanity-check the real
      generated question + explanation
- [ ] Re-verify the view/submit/grade flow in the browser against the live
      question
- [ ] Check off v0.1 in README.md and write the reconstruction prompt
- [ ] Visually confirm v0.4 (`/progress` dashboard) and v0.9 (Growtopia theme)
      in an actual browser (servers running at :8000/:3000) — no headless
      browser was available this session to do it directly. Once confirmed,
      check off both in README.md and write their reconstruction prompts.

## Backlog (out-of-scope for current version — don't build yet)

- [ ] Gamification Concepts 2 & 3 (streaks/daily goals, XP/levels/mastery
      badges) — deferred indefinitely. Only Concept 1 (stats dashboard, v0.4)
      is scheduled. If revisited, must honor the same hard constraints:
      never influence/be influenced by grading logic, never reward
      speed/guessing, live only on `/progress` (no mid-practice popups).

---

## Key Decisions Log

| Date         | Decision           | Reasoning |
| ------------ | ------------------ | --------- |
| 2026-08-09   | Backend: FastAPI + SQLite (stdlib sqlite3, no ORM) + uv | SQLite is enough for a single-question loop; defers Postgres+pgvector setup to v0.5 (dedup, renumbered from v0.4 on 2026-08-09) when dedup actually needs vector search. uv chosen over poetry (fast, single lockfile). |
| 2026-08-09   | Frontend: minimal Next.js (App Router, TS) + npm, no styling library | Sets up the real frontend framework now (per CLAUDE.md's recommendation) instead of a throwaway static page, avoiding a migration before v0.5's timed-test UI. npm avoids an extra package-manager install. |
| 2026-08-09   | v0.1's generation step uses the real Anthropic API (not hand-authored content) | "Prove the generate→verify→grade loop works" means proving the actual generation mechanism, not just the serving/grading UI. |
| 2026-08-09   | Added GENERATION_MODE=mock/live config flag; default mock | User wanted to test the app without spending on the Anthropic API. Mock mode serves 3 hand-authored static questions; live mode is the original untouched pipeline. v0.1 isn't considered done until live mode is actually run and verified. |
| 2026-08-09   | Gamification scoped to Concept 1 only (stats dashboard); placed at v0.4, right after filtered practice (v0.3) — dedup/full-assembly/scoring/deploy shifted down one to v0.5-v0.8 | Dashboard's purpose is motivating continued practice; "accuracy by type" pairs directly with v0.3's filtered practice ("go practice your weak type"), so it should land early rather than after every core feature ships. Streaks/XP/badges (Concepts 2 & 3) deferred to Backlog. |
| 2026-08-09   | Growtopia-inspired visual theme placed at v0.9, its own version after deploy | Cosmetic/CSS-only, orthogonal to v0.4's dashboard logic and applies app-wide (not just the dashboard), so kept as a separate reviewable unit; needs v0.4's `/progress` page to exist first, so sequenced after it. Press Start 2P restricted to headings/stat numbers only (illegible at small sizes) — nav/buttons/badges use a legible rounded sans font instead, keeping the pixel-chunky identity via borders/textures/palette/block-buttons rather than font alone. |
| 2026-08-09   | Concrete v0.9 palette: parchment `#fbf3dd` page bg, wood-brown `#8b5a2b` panels (shadow `#4a2f17` / highlight `#c68b4a` bevel edges), grass-green `#388e3c` primary buttons, sky-blue `#2a78d6` secondary buttons (reused from the dashboard's already-validated series color), fixed status green/red (`#0ca30c`/`#d03b3b`) for correct/incorrect only. All chosen with the dataviz skill's `validate_palette.js` — every text-on-fill and data-series-vs-surface pairing clears >=3:1 contrast in both light/dark; status green/red fails the CVD-separation check (expected/documented in the skill itself) so the UI never conveys correct/incorrect by color alone, always with a text label too. | Originally proposed palette (proposal turn) was directional only; this session made it concrete and checked it against real contrast math instead of eyeballing, per the dataviz skill's explicit instruction to validate rather than reason about it. |
| 2026-08-09   | Split "chrome" vs "reading" surfaces: `.clean-card` (plain white/light, system font) wraps stimulus/question stem/answer choices AND the post-grade explanation; a small `.result-chip` (themed, wood-bordered) carries only the short correct/incorrect + answer-letter status | The user's constraint was "clean reading area, themed frame around it." Explanation text is long-form reading content like the stimulus, so it stays in the clean card; the correct/incorrect verdict is short status text, so it's themed like the rest of the chrome. |
| 2026-08-09   | v0.4 and v0.9 built this session despite v0.1 still being incomplete/blocked | Explicit user instruction ("proceed") to work on unblocked, independent work while v0.1 waits on an `ANTHROPIC_API_KEY` from the user — a deliberate exception to the "finish current version first" convention, not a default to repeat without similar explicit direction. |

---

## Reconstruction Prompts Index

> One entry per completed version. Full prompt text lives in that version's entry
> below in the Session Log — this table is just a lookup.

| Version | Date completed | Reconstruction prompt location |
| ------- | -------------- | ------------------------------ |
| v0.1    | [YYYY-MM-DD]   | [link/anchor to entry below]   |

---

## Session Log

> Newest entry at the top. Tag each entry with the version it belongs to.

### [process/docs] Session 3 — 2026-08-09

**Prompt(s) used:**

```
From now on, formalize "finishing a version" as a defined checklist, and
update CLAUDE.md's Workflow Notes to encode it explicitly... [6-step
checklist: update prompt.md, check off README, write reconstruction prompt,
commit code+docs together with a version-naming commit message, tag with
the version number, push commit+tag]. Do not run this checklist for
work-in-progress states... ask if unsure. Show me the updated section
before committing that change.

please after finishing a version give me a checklist and if I confirm that
everything is correct, push to my github repo with the version name as the
note

please push everything to my github repo and use the version as the note
[clarified via question: nothing had cleared the "genuinely complete" bar
yet, so pushed as a plain checkpoint commit with no version tag, per user
choice]

please update all files including prompt.md and readme.md and then repush
back up to github based on where we currently are in this project
```

**What was done:**

- Formalized the "finishing a version" checklist into `CLAUDE.md`'s Workflow
  Notes (7 steps: update `prompt.md` → check off `README.md` → write
  reconstruction prompt + Reconstruction Prompts Index row → **present the
  user a checklist and stop for explicit confirmation** → commit → annotated
  tag with the version name as the tag's note/message → push commit + tag).
  Replaced the old looser bullets about reconstruction prompts/README
  checkboxes. Showed the section for review before committing, per
  instruction.
- Added a standing rule (confirm before any commit/tag/push, not just
  version-completion ones) after the user's follow-up. Saved this as a
  cross-session feedback memory
  (`feedback_git_push_confirmation.md`, outside this repo) so it persists
  beyond `CLAUDE.md` alone.
- Did the **first-ever commit and push** for this repo's real content.
  Nothing had cleared the "genuinely complete" bar (v0.1 blocked, v0.4/v0.9
  unverified in a browser — see Session 2), so per the checklist's own rule
  this could not be a version-tagged push; asked the user how to label it
  (`AskUserQuestion`) rather than guessing, and they chose a plain checkpoint
  commit with no tag. Committed all of v0.1 + v0.4 + v0.9's code plus the
  `CLAUDE.md` checklist update as commit `96dbc78` ("checkpoint: v0.1 app
  (mock mode) + v0.4 dashboard + v0.9 theme (WIP, unverified)") and pushed to
  `github.com/ripken808/LSAT-Prep` on `main`. Verified `.gitignore` actually
  excludes `frontend/.env.local` and `backend/data/` before staging, and that
  the one `.env`-pattern file that did get staged (`backend/.env.example`)
  only ever contained a placeholder (no real key was ever supplied this
  session).
- Docs-sync pass (this entry's trigger): filled in every placeholder section
  of `CLAUDE.md` that had concrete answers available but was never updated —
  Tech Stack, Commands, Coding Conventions, Do NOT touch, PR/Commit
  Conventions — and refreshed Project Structure to match the actual current
  file tree (v0.4/v0.9 additions weren't reflected there before). Filled in
  `README.md`'s Getting Started with real install/run commands. Fixed a
  factual error in `prompt.md`'s Current State (said `Branch: master`; the
  actual branch has been `main` since the repo's very first commit).

**What broke / what to watch:**

- Nothing code-level changed this session — docs and process only. Backend
  test suite untouched, not re-run (no code changed to invalidate it).
- v0.1 and v0.4/v0.9's respective blockers (API key; browser verification)
  are still open — this session didn't address either, just formalized
  process and synced documentation to reality.

**Next session should:**

- Same as Session 2's handoff: get an `ANTHROPIC_API_KEY` to finish v0.1,
  and get a real browser check on v0.4/v0.9 before checking either off.
- Once any version is genuinely complete, follow the now-formal checklist in
  `CLAUDE.md` → Workflow Notes exactly: prep steps 1-3, present a checklist,
  wait for confirmation, then commit/tag/push.

**Reconstruction prompt (only if this session completed a version):**

```
Not applicable — this session didn't complete a version (process/docs work
only).
```

---

### [v0.4 + v0.9] Session 2 — 2026-08-09

**Prompt(s) used:**

```
[Gamification scoping] I want to gamify the practice experience... propose
2-3 concrete gamification concepts... Hard constraints: never influence/be
influenced by grading, don't incentivize guessing/rushing, keep visually
separate from question/grading UI, implement as its own new version(s) in
prompt.md, don't build until scope is agreed.

[Two-part build request] Two things to scope and build, in order — propose
before building either.
PART 1 — Gamification (Concept 1 only): attempts table (question_id,
selected_answer, correct, explanation_viewed, answered_at) written by
grading as a pure side effect, grading logic unchanged; /progress page
(overall accuracy, accuracy by type, attempts over time), own nav link,
never shown during a question. Recommend version placement among the
remaining core versions.
PART 2 — Growtopia-inspired visual theme: pixel-art aesthetic, chunky
wood-panel buttons/panels, bright saturated colors, playful pixel font for
chrome. Original assets only (no sourced/copied Growtopia sprites/logos/
trademarks, no "Growtopia" branding anywhere). Applies to nav/buttons/
progress dashboard/general chrome; the question-reading screen (stimulus/
choices) stays clean, high-contrast, unstyled. Cosmetic/CSS-only - no
grading/generation/data-model changes. Propose palette/button-style/fonts/
themed-dashboard-look and version placement before implementing.

[Approval with 2 changes] Approved. 1) Move dashboard to v0.4 (right after
v0.3), not v0.8 after deploy — motivates practice early, pairs with filtered
practice; renumber dedup/full-assembly/scoring/deploy down one. 2) Reserve
Press Start 2P for headings/large stat numbers only (illegible small) — use
a legible rounded sans for nav/buttons/badges elsewhere. Update prompt.md's
Version Plan with the corrected placement, then proceed.
```

**What was done:**

- Updated `prompt.md`'s Version Plan: inserted v0.4 (stats dashboard) right
  after v0.3, renumbered dedup/full-assembly/scoring/deploy to v0.5-v0.8,
  added v0.9 (Growtopia theme) after deploy. Added Backlog entry noting
  Gamification Concepts 2 & 3 (streaks, XP/badges) are deferred indefinitely.
- **v0.4:** Added `attempts` table to `backend/app/db.py` (question_id,
  selected_answer, correct, explanation_viewed, answered_at) plus
  `insert_attempt()`, `get_overall_stats()`, `get_stats_by_type()`,
  `get_attempts_by_day()`. Fixed `get_connection()` to use
  `executescript()` (was `execute()`, which breaks on multi-statement SQL
  now that there are two `CREATE TABLE`s). Wired `POST
  /api/question/{id}/grade` to insert an attempt row as a documented side
  effect *after* computing the deterministic correct/incorrect result —
  grading logic itself is untouched, zero read-back dependency.
  `explanation_viewed` is always `True` because this UI shows the
  explanation as part of the same grade response (no separate reveal
  step). Added `GET /api/stats/summary` (overall/by_type/over_time) with
  Pydantic models in `app/models.py`. Added `tests/test_stats.py` (4 tests:
  empty state, attempt recorded correctly, failed grade requests record
  nothing, multi-type aggregation is correct) — 9 tests total, all passing.
  Frontend: nav bar in `layout.tsx` (Practice/Progress links), new
  `app/progress/page.tsx` (stat tile + meter for overall accuracy, bar-table
  rows for accuracy-by-type and attempts-over-time, with a real `<table>`
  under the bars per the dataviz skill's table-view requirement). Loaded the
  **dataviz skill** before building any chart UI; used its reference
  palette (single blue hue for magnitude, not a rainbow) as the v0.4
  default, structured as CSS custom properties per its guidance so v0.9
  could re-theme by swapping token values only.
- **v0.9:** Added two Google Fonts via `next/font/google` in `layout.tsx` —
  Press Start 2P (`--font-pixel-display`, headings + stat-tile hero numbers
  only) and Fredoka (`--font-chrome-sans`, nav/buttons/badges/dashboard
  labels). Defined a full Growtopia-inspired token set in `globals.css`
  (parchment page background, wood-brown panel/border/bevel colors, grass-
  green primary + sky-blue secondary buttons, fixed status green/red for
  correct/incorrect) for both light and dark mode. **Validated the palette
  with the dataviz skill's `scripts/validate_palette.js`** rather than
  eyeballing it — confirmed >=3:1 contrast for text-on-wood, text-on-button,
  and the dashboard's blue series against the new parchment/dark-wood
  surfaces; confirmed (and designed around) the expected CVD-separation
  failure between the fixed status green/red by ensuring the UI always
  pairs that color with a text label ("Correct!"/"Incorrect."), never color
  alone. Added reusable `.wood-panel`, `.block-btn` (+ `-primary`/
  `-secondary`), `.result-chip` (+ `-correct`/`-incorrect`) classes; re-skinned
  nav, buttons, `/progress` panels and bars via the v0.4 CSS-variable tokens
  (component CSS mostly untouched — only token values changed). Added a
  `.clean-card` class (plain white/light background, system font) and
  restructured `app/page.tsx` so the stimulus/question stem/answer choices
  AND the post-grade explanation render inside it — long-form reading
  content stays untouched by the pixel theme, per the hard constraint. Only
  the short correct/incorrect verdict became a themed `.result-chip`.

**What broke / what to watch:**

- `conn.execute(SCHEMA)` broke once `SCHEMA` held two `CREATE TABLE`
  statements (`sqlite3.ProgrammingError: You can only execute one statement
  at a time`) — fixed by switching to `conn.executescript(SCHEMA)`. Worth
  remembering if `SCHEMA` grows again.
- **Neither v0.4's dashboard nor v0.9's theme has been visually confirmed in
  an actual rendered browser.** No headless browser was available in this
  environment (chromium cask installed but the `.app` binary is missing).
  Verification stopped at: pytest (backend), curl (real data flow), and
  confirming both pages compile with no errors and the correct CSS
  classes/font variables appear in server-rendered HTML. Per CLAUDE.md's
  "test the UI in a browser before claiming success" convention, this is
  disclosed rather than glossed over — **do not check off v0.4 or v0.9 in
  README.md until a real browser confirms they render as intended.**
- v0.1 is still blocked/incomplete (unchanged from Session 1) — this
  session's work was explicitly authorized to proceed ahead of it.

**Next session should:**

- Get the user (or a working browser) to visually confirm `/` and
  `/progress` at `http://localhost:3000` render correctly — nav, chunky
  wood-panel buttons/dashboard, clean reading card, correct/incorrect chip.
- Only after that: check off v0.4 and v0.9 in `README.md` and write their
  reconstruction prompts.
- Separately: still need an `ANTHROPIC_API_KEY` to finish v0.1 (see Session
  1 handoff, still outstanding).

**Reconstruction prompt (only if this session completed a version):**

```
Not written — neither v0.4 nor v0.9 has been visually confirmed in a
browser yet (see What broke / what to watch above).
```

---

### [v0.1] Session 1 — 2026-08-09

**Prompt(s) used:**

```
Read CLAUDE.md and prompt.md for full project context... Your task is v0.1...
generate one original Logical Reasoning question..., determine the correct
answer, and write an explanation that applies the official named LSAT
methodology... Verify the answer using the independent re-solve check...
Then build the minimal path for me to see the question, submit an answer, and
get it graded... Before writing any code: propose a plan...

[Follow-up, before live generation was run:]
For now, I want to test the app without spending any money on the Anthropic
API. Add a mock/seed-data mode rather than calling the live API: hand-write
2-3 static LR questions as seed data; add a GENERATION_MODE env var
(default "mock") gating mock vs. live serving; do NOT delete/rewrite/simplify
the existing live generation/verification code, just gate it behind
GENERATION_MODE=live; update the seeding script for mock mode with no API key
required; update prompt.md's Current State to note mock mode and that v0.1 is
NOT complete yet (the actual goal was proving the live loop with real API
calls) — do not check off v0.1 in README.md until GENERATION_MODE=live is run
and verified end-to-end.
```

**What was done:**

- Planned and built the full v0.1 app: `backend/` (FastAPI + SQLite via
  stdlib `sqlite3`, `uv`-managed) and `frontend/` (minimal Next.js 16 App
  Router page, `npm`-managed).
- Backend: `questions` table (section, question_type, content_area,
  stimulus, question_stem, choices, correct_answer, explanation, verified,
  created_at); `GET /api/question/current` (no answer/explanation exposed);
  `POST /api/question/{id}/grade` (deterministic key match, always returns
  the stored explanation); `POST /api/generate` (live pipeline wrapper).
- Live generation pipeline (`app/generation.py`, `app/prompts.py`): one
  Anthropic API call to generate a question (system prompt embeds the full
  named-methodology reference for all 14 official LR types from CLAUDE.md),
  a second fresh-context API call to independently re-solve it, retry up to
  3x on mismatch. This code was written but has NOT yet been run against the
  real API (see Blockers above).
- Frontend: single unstyled page — fetch current question, radio choices,
  submit, display correct/incorrect + stored explanation.
- Backend tests: `pytest` suite (`tests/test_grading.py`, 5 tests) covering
  grading determinism, unknown question id, invalid answer letter, and that
  `/api/question/current` never leaks the answer/explanation. All passing.
- **Follow-up (mock mode):** added `backend/app/mock_questions.py` with 3
  hand-authored questions (necessary_assumption, flaw, parallel_reasoning),
  each with a methodology-correct explanation (negation test / named flaw
  taxonomy / abstracted structure matching, respectively). Added
  `GENERATION_MODE` config flag (`app/config.py`, default `"mock"`). Gated
  `POST /api/generate` behind `GENERATION_MODE=live` (returns 400 in mock
  mode). Updated `scripts/generate_question.py` to branch: mock mode wipes
  and reseeds the 3 static questions (no API key needed); live mode is the
  original, untouched `generate_and_verify()` call. Ran the seeding script in
  mock mode and manually verified the full view → submit → grade flow in the
  browser against the mock questions (both correct and incorrect submissions
  confirmed working via curl and the UI).
- Removed the empty placeholder `src/` dir; added root `.gitignore`.

**What broke / what to watch:**

- The live generate→verify pipeline has never actually been exercised against
  the real Anthropic API — it's implemented and unit-testable at the
  parsing/validation level but genuinely unverified end-to-end. This is the
  main open risk for v0.1: prompt reliability (valid JSON, exactly 5
  choices, plausible distractors) and the retry-on-mismatch logic are
  unproven until run for real.
- `backend/.env*` and `backend/.env.example` are covered by a permission
  deny-rule in this environment (Claude Code can't Read/Edit them) — had to
  work around this by not touching `.env.example` further; it still
  documents only `ANTHROPIC_API_KEY=` (GENERATION_MODE default of "mock" is
  handled in code, so this doesn't block mock mode).

**Next session should:**

- Get an `ANTHROPIC_API_KEY` from the user, set `GENERATION_MODE=live` in
  `backend/.env`, run `scripts/generate_question.py`, and manually sanity-check
  the generated question's methodology/explanation quality.
- Verify the full view → submit → grade flow in the browser against a
  live-generated question.
- Only then: check off v0.1 in `README.md`, update Version Plan status to
  done, and write the required reconstruction prompt.

**Reconstruction prompt (only if this session completed a version):**

```
Not written — v0.1 is not yet complete (see Current State / Blockers above).
```
