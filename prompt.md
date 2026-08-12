# Project Log — LSAT Prep

> Working memory that survives context compaction and new sessions. @-mention this
> file at the start of every Claude Code session. Update it at the END of every
> session, before closing out. See `CLAUDE.md` for stable project conventions,
> versioning strategy, and the reconstruction prompt requirement.

---

## Current State (overwrite this section each time — don't append)

- **Current version:** v0.7 (scaled score conversion, 120-180) — **complete,
  pending the user's confirmation before commit/tag.** Eight versions done, in
  this actual order:
  v0.4 -> v0.9 -> v0.1 -> v0.2 -> v0.3 -> v0.5 -> v0.6 -> v0.7.
- **v0.7 final state.** `app/scoring.py` holds the whole version as pure
  functions with no I/O: a `CONVERSION_TABLE` mapping raw-out-of-76 to 120-180,
  `PERCENTILE_ANCHORS` for an interpolated percentile, and
  `scaled_score` / `percentile_band` / `is_estimated`. `POST /api/test/grade`
  gained three fields (`scaled_score`, `percentile`, `scaled_is_estimated`);
  grading logic itself is untouched. The `/test` results screen now headlines
  the scaled score, reusing `/progress`'s existing `.stat-tile` classes — no new
  CSS. 76 tests, up from 51.
- **The central problem it solves: the test is 52 questions, the scale is built
  for 76.** Reading 31 straight off a 76-item table would score it as 41% when it
  is really 60% — a ~11-point scaled error. So `scaled_score` normalizes to a
  percentage first, converts to an equivalent raw out of 76, and then looks up.
  `is_estimated(total)` returns `total != 76`, so the "Estimated score" label
  flips to "Scaled score" on its own the day RC expansion makes a blueprint-
  length paper possible — no code change needed.
- **Two accuracy bugs found and fixed during the build, both in the percentile,
  both invisible to a passing test suite.** (1) Bucketing to the nearest 5-point
  anchor and taking the floor understated the middle of the curve badly: a 154
  reported "~45th percentile" when the real figure is ~62nd, because five scaled
  points span ~20 percentile points there. Fixed by interpolating between
  anchors. (2) The top anchor is 99.9, which `round()` turned into a
  "~100th percentile" — a percentile that cannot exist. Now capped to
  "99th percentile or above".
- **Verified end to end in a real browser** with Playwright clock control:
  started a test, answered part of section 1, fast-forwarded through all three
  section expiries, and the results screen rendered the scaled score, percentile
  and caveat correctly with zero console errors. Separately confirmed the whole
  curve through the live API (26/52 -> 148, 31/52 -> 154, 36/52 -> 160,
  47/52 -> 174, 52/52 -> 180).
- **The verification did not pollute practice data.** Grading a paper against the
  running app writes real `attempts` rows, so `backend/data/lsat_prep.db` was
  backed up to the scratchpad first and restored afterward — confirmed back at
  5 attempt rows. Worth repeating for any future browser verification that
  submits a test.
- **Repo status:** v0.7 is **not yet committed or tagged** — awaiting user
  confirmation per the Finishing a Version checklist. Seven prior versions are
  pushed and tagged on `github.com/ripken808/LSAT-Prep`. The working tree also
  carries a small CLAUDE.md doc fix from the start of this session (stale route
  list, Python version wording), intended to ride along with the v0.7 commit.
- **Branch:** main
- **Blockers:** none. Next candidates are v0.8 (deploy — the last core feature
  and the actual point of the project), RC content expansion (which would unlock
  the blueprint preset and flip v0.7's estimate label to exact), or the
  structural tell checker from v0.5's Backlog.

---

## Version Plan

> Small, explicitly-scoped versions — see Versioning Strategy in CLAUDE.md. Don't
> start a version until its scope is written here. Mark complete only when it works
> end-to-end for its stated scope.
>
> **Version numbers are stable scope IDs, NOT build order.** They have never
> matched the order things were actually built, and the "Build order" column below
> is the honest record. Two things caused the drift: (1) v0.4 and v0.9 were built
> and completed ahead of v0.1 by explicit user authorization, because v0.1 was
> blocked waiting on an `ANTHROPIC_API_KEY` and they were unblocked, independent
> work; (2) v0.1 then completed only after its scope was *revised* to drop the
> live-API requirement, not after the blocker cleared. The numbers are deliberately
> NOT being renumbered to match: `v0.1`/`v0.4`/`v0.9` are annotated tags already
> pushed to GitHub, and every reconstruction prompt cross-references these numbers,
> so renumbering would invalidate published history to fix a cosmetic problem.
>
> Practical consequence to keep in mind when reading the reconstruction prompts:
> v0.2's RC page reuses v0.9's `.clean-card` / `.block-btn` / `.result-chip`
> classes and needed no new CSS — because v0.9 was already finished and tagged
> before v0.2 was started. A lower version number does not mean "built on less."

| Version | Scope                                                                                                                                                                                                                                                                  | Status          | Build order |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ----------- |
| v0.1    | **REVISED 2026-08-09.** Store a hand-authored, independently-verified Logical Reasoning question bank (no live Anthropic API required) covering multiple official LR question types, with answer key + methodology-based explanation per question; serve a random question and grade a user's answer against it. Verification method: fresh subagent re-solves each question with no memory of the marked answer; only keep on match. The original live-API generate/verify pipeline remains in the codebase as an optional future path, not required for this version. No dedup check yet, no UI polish, no filtering, no full-length test. | [x] DONE — 2026-08-09, 14 questions (all 14 official LR types), 11/11 independently verified, random-serve bug fixed | **Written 1st** (Session 1, base app) but **completed 3rd** — tag `v0.1` = `7f6cbd3`, 2026-08-09 19:06. Sat incomplete across Sessions 1-4 while blocked on an API key; finished only once its scope was revised. |
| v0.2    | **REDUCED STARTER SCOPE 2026-08-09.** Add Reading Comprehension: hand-authored, independently-verified passages + questions (same method as v0.1's revised approach — no live API). New `passages` table + `passage_id` FK; new RC question-type taxonomy (10 types); `GET /api/passage/random` (passage + all its questions); reuses existing grade endpoint. Started at 2 passages (law, natural_science) x 5 questions instead of the originally proposed 4 passages x 5 — deliberately smaller to validate the approach first; more content areas can be added the same way later (see Backlog). No Analytical Reasoning — not part of the current real LSAT (removed Aug 2024). | [x] DONE — 2026-08-09. 2 passages, 10 RC questions, 10/10 independently verified; re-verified in Session 8 (13/13 pytest, live API smoke test, `tsc --noEmit` + `npm run build` clean) | **Written 4th, completed 4th** — tag `v0.2`, 2026-08-09. Built on top of finished v0.4 + v0.9, so it reused their CSS classes rather than adding any. |
| v0.3    | **REVISED 2026-08-10.** Filtered practice mode: `GET /api/taxonomy` (types + content areas with live counts) and `GET /api/questions/filtered` (multi-select by section/type/content area, whole matching set returned in random order), plus a `/focus` page that cycles the filtered set. Metadata tagging — the original half of this version's scope — was already satisfied by v0.1/v0.2 and needed no work. Scope was **extended** to expand the LR bank from 1 to **3 questions per type (42 total, 28 new)**, because filtering to a single type otherwise returned a pool of one. Includes a strengthened two-pass verification protocol and bank-level tell removal. | [x] DONE — 2026-08-10 | **Written 5th, completed 5th.** 42 LR + 10 RC = 52 questions. 31 questions verified by blind re-solve + adversarial distractor pass; 19 re-verified again after editing. |
| v0.4    | Practice stats dashboard (Gamification Concept 1 only — no streaks/XP/badges): `attempts` table (question_id, selected_answer, correct, explanation_viewed, answered_at) written by the grading endpoint as a pure side effect — grading logic itself does not change, zero read dependency on this data. `/progress` page (own nav link, never shown during a question): overall accuracy, accuracy by question type, attempts over time. | [x] DONE — 2026-08-09, visually confirmed via Playwright screenshots | **Written 2nd, completed 1st** — the first version ever finished. Tag `v0.4` = `6725b0b`, 2026-08-09 18:35. Built on top of an *incomplete* v0.1. |
| v0.5    | **REVISED 2026-08-10.** Near-duplicate detection over the question bank: `app/similarity.py` (text selection, cosine similarity, pair ranking, lazy model load), an `embeddings` cache table keyed by content hash, and `scripts/check_duplicates.py` reporting the closest pairs. Local embeddings (`BAAI/bge-small-en-v1.5`) behind an optional `dedup` extra — no API key, no spend, and the app and test suite never need PyTorch. Rescoped from "gate live generation" to an **authoring-time** check, because the app has no runtime generation to gate. No Postgres/pgvector. | [x] DONE — 2026-08-10. Reports pairs; caches by content hash. **Does not detect the structural/architectural duplication that motivated it — see the Backlog item and Session 10.** | **Written 6th, completed 6th** — tag `v0.5`, 2026-08-10. |
| v0.6    | **REVISED 2026-08-11.** Full-length timed practice test: `app/assembly.py` (section presets, no-repeat sampling across the whole paper, LR spread across question types, RC assembled by whole passage), `GET /api/test/new`, `POST /api/test/grade` (batch, blank = incorrect), and a `/test` page with a hard 35-minute cutoff per section, free navigation within a section, no feedback until submission, and raw-score + per-question review. **Ships at REDUCED section sizes (21/21/10) because the bank cannot fill a real blueprint** — a `blueprint` preset exists and refuses with a countable shortfall until the content is there. State is in-memory; a reload loses the test. | [x] DONE — 2026-08-11. Verified end to end in a browser including real timer expiry auto-advancing all three sections. | **Written 7th, completed 7th** — tag `v0.6`, 2026-08-11. |
| v0.7    | **SCOPED 2026-08-12.** Scaled score conversion (120-180): `app/scoring.py` (pure functions — a raw-out-of-76 conversion table, interpolated percentile anchors, `scaled_score`/`percentile_band`/`is_estimated`), three additive fields on `POST /api/test/grade`, and a reworked `/test` results panel that headlines the scaled score plus an approximate percentile. Because the paper runs at reduced length (52 vs ~76), the raw score is **normalized to a percentage before conversion** and the result is labelled an estimate. Deliberately excludes score persistence/history, any `/progress` change, and scaled scoring on single-question or `/focus` practice. | [x] DONE — 2026-08-12. 76 tests, up from 51. Browser-verified end to end; full curve confirmed through the live API. | **Written 8th, completed 8th** — the first version whose number matches its build position. |
| v0.8    | Deploy so friend can access it online                                                                                                                                                                                                                                  | [ ] not started | Not started, order undecided — and note v0.9 (numbered *after* it) is already done, so this number in particular implies nothing about sequence. |
| v0.9    | Growtopia-inspired visual theme (cosmetic/CSS-only — no grading/generation/data-model changes). Original pixel-chunky UI: wood-panel borders/textures, beveled 3D block buttons, bright saturated palette, applied to nav, buttons, general chrome, and the themed `/progress` dashboard. Press Start 2P reserved for headings/large stat numbers only; a legible rounded sans font for nav links, button labels, and badge text. The question-reading screen (stimulus/stem/choices) stays clean, high-contrast, unstyled by the pixel theme. | [x] DONE — 2026-08-09, visually confirmed via Playwright screenshots | **Written 3rd, completed 2nd** — same commit/tag moment as v0.4 (`6725b0b`, 2026-08-09 18:35), since both were verified together in Session 4. Completed *before* v0.1 and v0.2 despite the highest number. |
| v0.x    | [add more as scope becomes clearer]                                                                                                                                                                                                                                    | [ ] not started | — |

---

## Next Up (current version's immediate tasks)

- [x] v0.2 confirmed done by the user and the full Finishing a Version
      checklist run: README box checked, Reconstruction Prompts Index row
      added, Version Plan status flipped to DONE, WIP commit amended into the
      final v0.2 commit, annotated tag `v0.2` created, commit + tag pushed.
- [x] `.claude/commands/` resolved: user chose NOT to track them. Added
      `.claude/commands/` to `.gitignore` as personal local slash commands.
- [x] v0.3 chosen and built 5th: filtered practice mode plus the LR bank
      expansion to 3 questions per type.
- [x] v0.5 built 6th: near-duplicate detection over the question bank.
- [x] v0.6 built 7th: full-length timed practice test at reduced section sizes.
- [x] v0.7 built 8th: scaled score conversion (120-180) on the `/test` results
      screen, with an interpolated percentile.
- [ ] Decide what gets built 9th. Live options: **v0.8** (deploy — the last core
      feature and the reason the project exists; a friend can't use localhost);
      **RC content expansion** (2 passages + ~17 questions, which would unlock
      v0.6's blueprint preset *and* flip v0.7's "Estimated score" label to an
      exact "Scaled score" with no code change); or the **structural tell
      checker** from v0.5's Backlog.
- [ ] Remaining Backlog: too-easy distractor rewrites, residual answer-length
      tell, `MOCK_QUESTIONS[2]` exemplar contamination, the two `/progress` bugs
      (orphaned attempts, UTC date bucketing), the empty-DB startup warning,
      `DB_PATH` not actually env-overridable, and score history (deferred out of
      v0.7).

## Backlog (out-of-scope for current version — don't build yet)

- [ ] Gamification Concepts 2 & 3 (streaks/daily goals, XP/levels/mastery
      badges) — deferred indefinitely. Only Concept 1 (stats dashboard, v0.4)
      is scheduled. If revisited, must honor the same hard constraints:
      never influence/be influenced by grading logic, never reward
      speed/guessing, live only on `/progress` (no mid-practice popups).
- [ ] Expand RC content beyond v0.2's 2 starter passages — add social_science
      and humanities passages (the other 2 of the original 4 real LSAT RC
      content areas), and cover the 2 RC types not yet used (rc_passage_
      organization, rc_analogous_situation). Same method: hand-author +
      independent subagent verification, then regenerate `prep.txt`.
- [ ] **BUG (pre-existing, v0.4 defect — reproduced live 2026-08-09):**
      orphaned `attempts` rows make `/progress` self-contradictory.
      `get_overall_stats()` counts every attempt row, but `get_stats_by_type()`
      JOINs to `questions` and silently drops attempts whose `question_id` no
      longer exists. The seed script wipes and reinserts `questions` with fresh
      autoincrement ids, but never clears `attempts`, and there's no
      `ON DELETE CASCADE`. Observed after a reseed: overall total = 7 while the
      by-type rows summed to 5. Fix is small — add `ON DELETE CASCADE` to the FK
      (plus a `PRAGMA foreign_keys = ON`, which sqlite3 does NOT enable by
      default), or have the seed script clear `attempts` alongside `questions`.
      NOT fixed during v0.2: it predates v0.2, belongs to v0.4's surface, and
      pulling it in would violate the Versioning Strategy. Do it as a small
      standalone fix or fold it into the next version.
- [x] ~~DATA ACCURACY (found Session 8): three questions' `verified` flag
      over-claimed.~~ **RESOLVED in v0.3** — LR 1-3 were put through the full
      two-pass protocol along with the 28 new questions.
- [x] ~~QUALITY (found Session 8): verification cannot detect weak distractors
      or an over-strong key.~~ **RESOLVED in v0.3** — the adversarial distractor
      pass now runs on every new question and is documented in the
      `lsat-methodology` skill. LR question 1's over-strong key was rewritten.
- [ ] **FOOTGUN: schema changes silently empty the app (2 incidents).** The
      schema uses `CREATE TABLE IF NOT EXISTS`, so it never alters an existing
      database — adding a table means deleting `backend/data/lsat_prep.db` and
      **reseeding**. Skip the reseed and the app comes up with a valid, empty DB
      and reports "No question has been generated yet." Hit in Session 6 (adding
      `passages`) and again in Session 10 (adding `embeddings`). Fix is small:
      have the app log a warning at startup when `questions` is empty, or add a
      `--check` flag to the seed script. Recovery is always
      `cd backend && uv run python scripts/generate_question.py`.
- [ ] **STRUCTURAL DUPLICATION — the defect v0.5 set out to catch and did not
      (measured 2026-08-10).** v0.5's embedding check ranks the known LR 0/14/15
      near-duplicate cluster at **79th, 216th, and 382nd of 861 LR pairs**
      (similarities 0.673 / 0.623 / 0.579) — far below its 0.80 threshold. This
      is not a tuning problem and no threshold fixes it: those three questions
      are about security cameras, museum finances, and bike-share, so they are
      genuinely dissimilar *in topic and wording*, which is all cosine
      similarity over text measures. What makes them duplicative is **answer
      architecture** — all three keys were the only hedged choice and all three
      traps the only absolute one, so "pick the hedged one" scored 3/3. Fix
      needs a different tool: a structural fingerprint over
      (question_type, answer wording shape, argument form), or simply
      generalizing the v0.3 tell measurements (letter distribution,
      answer-length, per-type architecture) into a `check_tells.py` that runs
      alongside `check_duplicates.py`. The measurements already exist as a
      checklist in the `lsat-methodology` skill; nothing automates them.
- [ ] **QUALITY, still open after v0.3:** the adversarial pass rated roughly a
      third of items "too_easy" (all four distractors dismissible on sight) and
      supplied concrete per-question rewrite suggestions — see the Session 9 log
      for the full list. Fixing these means authoring better traps, not more
      questions. Also still open: the answer-length tell was reduced from 76% to
      57% of keys being the longest choice, with max margin down from 118 to 38
      characters; the residual is mostly 1-2 character differences and no longer
      exploitable, but a full pass would bring it to the ~20% baseline.
- [ ] **CONTAMINATION (found Session 9):** the parallel_reasoning question at
      `MOCK_QUESTIONS[2]` is *verbatim* the reference example in
      `.claude/skills/lsat-methodology/SKILL.md` and in `prompts.py`'s
      `REFERENCE_EXAMPLE_BLOCK`. Two consequences: it is by definition
      memorizable, and any verifier that loads the skill sees its marked answer
      before solving, so re-solving it is not genuinely independent. Fix: author
      a distinct served question and keep the exemplar teaching-only.
- [ ] **ADVERSARIAL SWEEP of the 11 remaining v0.1 questions** that were only
      ever single-pass verified (indices 3, 6, 7, 8, 12 and the rest of the
      original 14 not covered in Session 9's re-check).
- [ ] **SCORE HISTORY (deferred out of v0.7, 2026-08-12):** v0.7 converts a raw
      score to 120-180 and displays it, but nothing is persisted — reload the
      results screen and the score is gone. A score-over-time view is the
      natural follow-on (a `test_results` table plus a chart on `/progress`),
      and was deliberately kept out of v0.7 to hold its scope. It is close to a
      version of its own; scope it as one rather than bolting it onto v0.8.
- [ ] **`DB_PATH` is not env-overridable (found 2026-08-12).** CLAUDE.md's Tech
      Stack describes `config.py` as "env loading (ANTHROPIC_API_KEY,
      GENERATION_MODE, DB_PATH)", but `DB_PATH` is a hardcoded constant —
      only the other two read from the environment. This bit during v0.7's
      browser verification: grading a test against the running app writes real
      `attempts` rows, and with no way to point the server at a scratch DB the
      only safe route was backing up and restoring `backend/data/lsat_prep.db`
      by hand. Fix is one line (`os.environ.get("DB_PATH", ...)`) and would make
      end-to-end verification non-destructive by default. Left alone during v0.7
      to hold scope.
- [ ] **BUG (minor, same root cause as the log-date confusion):** `answered_at`
      is stored as UTC and `get_attempts_by_day()` groups on `substr(answered_at,
      1, 10)`, so `/progress`'s "attempts over time" buckets by **UTC** date.
      For a US-Pacific user, anything practiced after 5pm local is charted on the
      next day. Confirmed live: attempts made 2026-08-09 evening PDT charted
      under `2026-08-10`. Decide on a timezone convention before v0.7/v0.8.

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
| 2026-08-09   | v0.1 revised: dropped the live-Anthropic-API requirement in favor of a hand-authored, independently-verified static question bank | User explicitly asked to move away from live AI generation to "verified used Questions" — clarified (after flagging copyright risk around real/official LSAT questions) to mean ORIGINAL questions, verified for correctness. Live pipeline code kept, untouched, as an optional future path. |
| 2026-08-09   | Verification method for new questions: fresh subagent (no memory of marked answer) independently re-solves each one; only keep on match | Mirrors the exact independent re-solve check already documented in CLAUDE.md's Explanation Methodology, just run by Claude Code during authoring instead of via a live API call from the running app — satisfies "no Anthropic API used" while preserving the same rigor. Result: 11/11 new questions matched on first pass. |
| 2026-08-09   | `GET /api/question/current` changed from "always the latest-inserted row" to "random row on every call" | User reported the app kept showing the same question after the bank grew to 14 — the endpoint had no concept of multiple questions since v0.1 was originally scoped around a single question. Minimal fix: `ORDER BY RANDOM() LIMIT 1` instead of `ORDER BY id DESC LIMIT 1`; kept the same route/URL to avoid frontend churn. |
| 2026-08-09   | v0.2 (RC) started at 2 passages instead of the originally proposed 4 | User chose "start smaller" to validate the passage/question data model and RC taxonomy before committing to a bigger authoring effort. Remaining 2 content areas (social_science, humanities) logged to Backlog, not built now. |
| 2026-08-09   | New `passages` table + nullable `passage_id` FK on `questions`, rather than duplicating passage text onto every question row | Multiple RC questions share one passage; normalizing avoids text duplication and lets `GET /api/passage/random` return the passage once with all its questions. `stimulus` on `questions` became nullable (RC questions have no stimulus of their own — their text lives on the joined passage). |
| 2026-08-09   | RC question types prefixed `rc_` (e.g. `rc_main_point`) even where conceptually similar to an LR type name | Keeps LR and RC fully distinct in the schema and in `/progress`'s accuracy-by-type breakdown — an LR "main point" question and an RC "main point" question aren't really the same skill, and prefixing avoids needing to touch v0.4's already-shipped stats query/model to disambiguate by section. |
| 2026-08-09   | RC practice flow is a separate `/reading-comp` page (passage read once, then its questions answered in sequence), not merged into LR's per-question-random flow | Real RC practice means reading a passage once and answering several questions about it in a row, not re-fetching/re-reading the same passage repeatedly under random per-question selection. Keeping LR (`/`) and RC (`/reading-comp`) as separate flows avoided restructuring the already-shipped LR page at all — pure addition. |
| 2026-08-09   | Added `prep.txt` (repo root) as a derived, regeneratable export of the full question bank, plus a standing CLAUDE.md rule to regenerate it after authoring any new question | User wants a plain-text study file that's always in sync. Regenerating from the canonical source files (`mock_questions.py`, `rc_content.py`) via a script avoids the drift risk of manually appending to the file by hand. |
| 2026-08-11   | v0.6 ships reduced section sizes (21/21/10), not the real blueprint | The blueprint is 2 LR of 24-26 plus RC of 26-28 across 4 passages; the bank holds 42 LR and 10 RC across 2 passages. A blueprint-accurate test would serve every RC question 2.7 times, which is not a practice test. User chose configurable sizes: ship what the bank supports with nothing repeated, keep a `blueprint` preset that refuses with a countable shortfall, and state the gap on the start screen rather than implying full length. |
| 2026-08-11   | Hard cutoff at 35:00 per section, auto-submit, no return; test state in-memory | Time pressure is most of what makes full-length practice worth doing, so a soft warning would defeat the purpose. Persistence across reload was considered and deferred — it needs a test-session table and resume logic, which is its own version. The start screen says plainly that a reload loses the test. |
| 2026-08-11   | RC sections are assembled by whole passage, never by sampling N questions | A passage is read once and answered against several times. Sampling questions independently would strand questions whose passage the test never shows. This mirrors how `/reading-comp` already works. |
| 2026-08-11   | `useCountdown` derives its value during render rather than in an effect | The obvious useState+useEffect shape returns a stale 0 on the first render after a new deadline is set, and the caller treats 0 as "time is up" — so starting a section instantly ended it. Found in the browser, not by the tests. The hook carries a comment saying not to simplify it back. |
| 2026-08-11   | A blank answer is scored incorrect but logs no attempt row | The real LSAT has no guessing penalty, but a blank is still wrong. Logging a non-attempt would distort `/progress`'s accuracy-by-type, which counts attempts. |
| 2026-08-12   | v0.7 normalizes the raw score to a percentage before converting, rather than looking it up directly | Real conversion tables map a raw score out of ~76 scored items; the reduced paper is 52. A direct lookup would read 31 as 31/76 (41%, ~143) when it means 31/52 (60%, ~154) — an ~11-point error understating every score. Normalizing costs one line and makes the same table correct at any test length. The alternatives considered and rejected: a score band (more honest about precision, but harder to track improvement against) and refusing to scale reduced tests at all (ships nothing usable, since `blueprint` currently 400s on a content shortfall). |
| 2026-08-12   | The conversion table is a representative composite curve, explicitly not a transcription of any published form's table | Real LSAT tables are equated per test form, so a given raw score maps to slightly different scaled scores on different tests — there is no single "the" table to copy, and presenting one as authoritative would overstate what this app can know. The docstring says so, and `is_estimated` keeps the UI honest about it. |
| 2026-08-12   | Percentiles are interpolated between 5-point anchors, not floored to the anchor below | The first implementation floored, which understated the middle of the curve badly: a 154 reported "~45th percentile" against a real ~62nd, because five scaled points span ~20 percentile points where the curve is steepest. A passing test suite would not have caught this — the bug was in the shape of the data, not the code. Also capped the top at "99th percentile or above", because rounding the 99.9 anchor produced a 100th percentile, which cannot exist. |
| 2026-08-12   | v0.7 scoped to conversion + display only; score persistence/history deferred to its own version | The Version Plan entry is "scaled score conversion", and a history view needs a new table plus dashboard work — pulling it in would repeat exactly the scope creep the Versioning Strategy exists to prevent. Logged to Backlog with a note that it is close to a version of its own. |
| 2026-08-10   | v0.5 rescoped from a runtime gate on generation to an authoring-time check over the hand-authored bank | Its stated job was gating generated questions, but the app has no runtime generation — the live pipeline in `generation.py` has never been run, so a runtime gate would be infrastructure with no traffic. The bank itself, however, is unmeasured, and v0.3's adversarial pass had already found near-duplicates in it. User chose the authoring-time scope. |
| 2026-08-10   | Local embeddings behind an OPTIONAL `dedup` extra; numpy promoted to a core dependency | Anthropic has no embeddings endpoint (checked against the current API surface via the `claude-api` skill), so this meant either a second vendor or a local model; user chose local. `sentence-transformers` pulls PyTorch — the venv goes from ~90MB to **790MB**, which is far too heavy to require for running the app or the tests. Making it an extra keeps `uv run pytest` working with no PyTorch installed (verified). I had told the user "~90MB model" when asking; that was the model file, not the dependency, and the correction is recorded here. |
| 2026-08-10   | Embedding model is `BAAI/bge-small-en-v1.5` (512-token context), not the obvious `all-MiniLM-L6-v2` | MiniLM truncates at 256 tokens. The bank's longest question — a parallel-reasoning item whose five choices are each full arguments — is 271 tokens, so it would have been silently cut. bge-small gives ~2x headroom at the same 384 dimensions. `embed()` now raises on any text over the model's limit rather than letting truncation pass silently. |
| 2026-08-10   | RC passages are deliberately NOT embedded | Two RC questions about one passage are intentionally different questions about shared material, not duplicates. Embedding the passage failed in two compounding ways: a ~555-token passage dwarfs a ~60-token stem, and it overflowed MiniLM's 256-token limit, so the embedded text was the first 256 tokens of the passage and nothing else — every question sharing a passage scored **exactly 1.000** and the stems never reached the model. A question's identity is its stimulus (LR), stem, and choices. |
| 2026-08-10   | pgvector deferred indefinitely; CLAUDE.md's "swap when v0.5 needs it" note rewritten | 52 vectors is a numpy dot product over a 52x384 matrix — sub-millisecond, no server, no new infrastructure. Leaving the old note would have had the next session standing up Postgres for a prototype's 52 rows. |
| 2026-08-09   | Corrected every `2026-08-10` date in this file to `2026-08-09` (Sessions 4-7 headers, 8 Key Decisions rows, the Reconstruction Prompts Index, and two Version Plan scope cells) | Every commit in the repo is dated 2026-08-09 (`git log`), so Sessions 4-7 could not have happened on the 10th. Root cause: `prep.txt`'s generated header reads `2026-08-10T02:36:54+00:00`, which is **UTC** — 19:36 PDT on 08-09 — and that UTC date got copied into the log as if it were the local session date. Sessions 1-3 correctly used local dates, so local is the convention. `prep.txt` itself was NOT changed: it's a derived export and its UTC timestamp is accurate. |
| 2026-08-09   | Version numbers are stable scope IDs, not build order; added an explicit "Build order" column to the Version Plan instead of renumbering | User noticed v0.2's RC page reuses v0.9's CSS classes, which is only possible if v0.9 was built first — correctly inferring the table's sequential look was misleading. True order: v0.4 and v0.9 completed 1st/2nd (`6725b0b`), v0.1 3rd (`7f6cbd3`), v0.2 4th. Renumbering was rejected because `v0.1`/`v0.4`/`v0.9` are annotated tags already pushed to GitHub and every reconstruction prompt cross-references those numbers — renaming would invalidate published history to fix a presentation problem. An explicit column keeps the record honest at zero cost to history. |

---

## Reconstruction Prompts Index

> One entry per completed version. Full prompt text lives in that version's entry
> below in the Session Log — this table is just a lookup.

| Completion order | Version | Date completed   | Tagged commit | Reconstruction prompt location |
| ---------------- | ------- | ---------------- | ------------- | ------------------------------ |
| 1st              | v0.4    | 2026-08-09 18:35 | `6725b0b`     | Session 4 entry below          |
| 2nd              | v0.9    | 2026-08-09 18:35 | `6725b0b`     | Session 4 entry below          |
| 3rd              | v0.1    | 2026-08-09 19:06 | `7f6cbd3`     | Session 5 entry below          |
| 4th              | v0.2    | 2026-08-09       | tag `v0.2`    | Session 6 entry below    |
| 5th              | v0.3    | 2026-08-10       | tag `v0.3`    | Session 9 entry below    |
| 6th              | v0.5    | 2026-08-10       | tag `v0.5`    | Session 10 entry below   |
| 7th              | v0.6    | 2026-08-11       | tag `v0.6`    | Session 11 entry below   |
| 8th              | v0.7    | 2026-08-12       | tag `v0.7` (pending) | Session 13 entry below |

Note on ordering: the completion order above is NOT the version-number order
— see the Version Plan's Build order column for the full explanation. v0.1
was completed chronologically AFTER v0.4 and v0.9 (its scope was revised
mid-project — see Key Decisions Log), so the commit tagged `v0.1` (`7f6cbd3`)
already contains v0.4's and v0.9's code, because it builds on the same linear
`main` history. Each reconstruction prompt below describes only its own
version's logical scope, for anyone who wants to rebuild just that layer —
so a prompt does not correspond to the full contents of its tagged commit.

---

## Session Log

> Newest entry at the top. Tag each entry with the version it belongs to.

### [v0.7] Session 13 — 2026-08-12 (scaled score conversion, 120-180)

**Prompt(s) used:**

```
/resume
fix these inconsistencies before continueing
lets continue where we left off
[AskUserQuestion picked v0.7 as the 8th version; three further scoping
decisions via AskUserQuestion: normalize-to-percentage over score-band or
raw-only, conversion+display only over persisting a score history, and
including an approximate percentile band]
```

**What was done:**

- **Session opened by reconciling docs against reality.** Two stale claims in
  CLAUDE.md were found and fixed before any code: the frontend build note still
  listed 4 routes (there are 6 — `/focus` and `/test` were never added) and
  still said "as of v0.2"; the Python line conflated the `>=3.11` floor with the
  3.14 the venv actually runs. Every other countable claim in the docs was
  checked against source and was accurate (42 LR / 2 passages / 10 RC / 52 total
  / 51 tests).
- **Surfaced the version's central problem before designing anything.** Real
  conversion tables are built for ~76 scored items; the reduced paper is 52. A
  direct lookup would have understated every score by ~11 points. The user chose
  percentage normalization, which makes one table correct at any length.
- Built `app/scoring.py` as pure functions with no I/O (same shape as
  `similarity.py`'s core), added three additive fields to `TestGradeResponse`,
  wired them in `grade_test` without touching grading logic, and reworked the
  `/test` results panel.
- **Reused rather than rebuilt.** The results panel headline uses `/progress`'s
  existing `.stat-tile` / `.stat-tile-value` / `.stat-tile-sub` classes — the
  first draft hand-rolled inline styles and a `--font-display` token that does
  not exist (it is `--font-heading`). No new CSS, holding v0.6's constraint.
- `tests/test_scoring.py` (22 tests) plus 3 endpoint tests appended to
  `test_assembly.py`. 76 total, up from 51.

**What broke / what to watch:**

- **Both real bugs this session were in the percentile, and both were invisible
  to a green test suite** — the defect was in the shape of the data, not the
  code. (1) Flooring to the nearest 5-point anchor understated the steep middle
  of the curve: 154 reported "~45th percentile" against a real ~62nd. Fixed by
  interpolating. (2) `round()` turned the 99.9 top anchor into a "100th
  percentile", which does not exist. Both were caught by *printing the actual
  curve and reading it*, not by a test. Worth doing for any lookup table.
- **Grading against the running app writes real `attempts` rows.** Browser
  verification submits a whole 52-question paper, which would have injected 52
  fake attempts into `/progress`. Handled by backing up
  `backend/data/lsat_prep.db` to the scratchpad and restoring after (confirmed
  back at 5 rows). The underlying cause — `DB_PATH` is hardcoded, not
  env-overridable despite CLAUDE.md saying otherwise — is logged to Backlog.
- One self-inflicted test failure: `scaled_score(5, 3)` asserted `None` but
  correctly raised, since 5 correct out of 3 is impossible. The guard was right,
  the test was wrong.
- Playwright is not a project dependency; it resolved only from the npx cache,
  so the verification script imports it by absolute path. Fine for a throwaway
  script, but a real frontend suite would need it installed properly.

**Next session should:**

- Pick the 9th version. **v0.8 (deploy)** is the last core feature and the actual
  point of the project — the friend cannot use localhost. **RC content
  expansion** is the highest-leverage content work: it unlocks v0.6's blueprint
  preset *and* flips v0.7's "Estimated score" to an exact "Scaled score" with no
  code change, since `is_estimated` keys off test length alone.

**Reconstruction prompt — v0.7 (scaled score conversion, 120-180):**

```
Rebuild this project (LSAT Prep) to v0.7's state. Everything in the v0.1, v0.2,
v0.3, v0.5 and v0.6 reconstruction prompts, PLUS raw-to-scaled score conversion
on the practice test's results screen.

SCOPE NOTE — READ FIRST: this is conversion AND DISPLAY ONLY. Do NOT persist
test results, do NOT add a score-history table or chart, do NOT touch
/progress, and do NOT add scaled scoring to single-question or /focus practice
— a scaled score is only meaningful for a whole test. Those are later versions.

THE CENTRAL PROBLEM: real LSAT conversion tables map a raw score out of ~76
scored items (2 LR sections of 24-26 plus RC of 26-28) onto 120-180. The bank
only supports a 52-question "reduced" paper. Looking a reduced raw score up
directly is WRONG and is the specific bug to avoid: 31 read as 31/76 is 41%
(~143), but it actually means 31/52, 60% (~154) — every score understated by
roughly 11 points. Normalize to a percentage FIRST, then convert.

app/scoring.py — pure functions, NO I/O, no DB, no network (mirrors the shape
of similarity.py's core so it is trivially testable):
- CANONICAL_ITEM_COUNT = 76.
- MIN_ITEMS_FOR_SCALING = 30. Below this, scaled_score returns None — a scaled
  score off a handful of questions is a number without a meaning, and
  /api/test/grade is reachable with any answer list, not just a whole paper.
- CONVERSION_TABLE: list[(minimum_raw_out_of_76, scaled)], descending, covering
  every scaled point 120-180 EXACTLY ONCE. Anchors: 75->180, 65->170, 53->160,
  40->150, 27->140, 17->130, 0->120. Make it a REPRESENTATIVE COMPOSITE curve
  and say so in the docstring — real tables are equated per test form, so there
  is no single authoritative table to copy, and presenting one as official
  overstates what the app can know.
- PERCENTILE_ANCHORS: list[(scaled, percentile)] every 5 points, 120->0.0 up to
  180->99.9 (150->45.0, 155->66.0, 160->81.0 are the ones that matter most).
- approximate_percentile(scaled): INTERPOLATE linearly between anchors. Do NOT
  floor to the anchor below — the curve is steepest in the middle where five
  scaled points span ~20 percentile points, so flooring reports a 154 as the
  150 anchor's ~45th when the real answer is ~62nd. This is a silent accuracy
  bug that a passing test suite will not catch.
- percentile_band(scaled) -> str: "below the 1st percentile" under 1%;
  "99th percentile or above" at 99%+ — do NOT let round() turn the 99.9 anchor
  into a "100th percentile", which cannot exist; otherwise "~62nd percentile"
  with a CORRECT ordinal suffix (11/12/13 take "th", not "st"/"nd"/"rd").
- scaled_score(correct, total) -> int | None: raise ValueError on negative
  inputs or correct > total; return None below MIN_ITEMS_FOR_SCALING; else
  round(correct / total * 76) and take the first matching table row.
- is_estimated(total) -> bool: total != CANONICAL_ITEM_COUNT. Keyed off test
  LENGTH, not a hardcoded flag, so the UI label corrects itself for free once
  the bank can fill a blueprint-length paper.

API — models.py adds three ADDITIVE fields to TestGradeResponse (change nothing
existing): scaled_score: int | None, percentile: str | None,
scaled_is_estimated: bool. main.py's grade_test populates them at the existing
return. GRADING LOGIC IS UNTOUCHED — same deterministic key match, same
attempt-logging side effect, blanks still incorrect and still log nothing.

FRONTEND — app/test/page.tsx results panel only:
- REUSE /progress's existing .stat-tile / .stat-tile-label / .stat-tile-value /
  .stat-tile-sub classes. Add NO new CSS. (The display font token is
  --font-heading; there is no --font-display.)
- Scaled score is the headline; percentile beneath it; raw count demoted to
  supporting text; the estimate caveat in .stat-tile-sub naming the actual
  question count vs ~76.
- Label reads "Estimated score" when scaled_is_estimated, "Scaled score"
  otherwise, and falls back to today's raw-only display when scaled_score is
  null.
- Delete the old "Scaled 120-180 scoring arrives in v0.7." line.

TESTING — tests/test_scoring.py, pure functions, no DB or fixtures:
- TABLE INTEGRITY FIRST: assert the conversion table covers 120-180 with no
  gaps or repeats and descends on both columns; assert percentile anchors ascend
  and span 120-180. A lookup table rots silently — a typo'd row still returns a
  plausible number.
- The version's whole point: 31/52 and 31/76 must differ by >= 5 scaled points.
- Equal percentages scale alike within 1 point regardless of test length.
- Interpolation: approximate_percentile(154) lands in 60-64, not ~45.
- No output anywhere on the scale contains "100th".
- Boundaries (0 -> 120, perfect -> 180), the None guard, the three ValueError
  cases, ordinal suffixes.
Plus endpoint tests in test_assembly.py: grade a REAL assembled paper (grade
once with all blanks to read the keys back, then re-grade) and assert the scaled
score is in range, that a perfect paper is 180 and a blank one 120, and that a
3-answer POST returns scaled_score: null.

VERIFY IN A BROWSER, and back up backend/data/lsat_prep.db first — submitting a
test writes real attempts rows and will otherwise pollute /progress with fake
data. DB_PATH is hardcoded, so there is no env override to point at a scratch
DB. Use Playwright clock.install() + fastForward('36:00') per section to reach
the results screen without answering 52 questions by hand.

NOT YET IMPLEMENTED as of v0.7: score persistence/history (no test_results
table — reload the results screen and the score is gone); deployment (v0.8); RC
content expansion, which would unlock v0.6's blueprint preset and flip
is_estimated to False on its own. The live Anthropic generate/verify pipeline
still exists and has still never been run.
```

---

### [process] Session 12 — 2026-08-12 (session close-out; push policy changed)

**Prompt(s) used:**

```
/end  — with the command file rewritten to be fully autonomous:
"execute the full checklist below with no confirmation steps and no questions
at the end... Push automatically — commit and any tags, with no confirmation
step, whether the version was complete or WIP. Do not ask before pushing."
```

**What was done:**

- **The standing push-confirmation rule was deliberately changed by the user.**
  `.claude/commands/end.md` previously ended with "Always ask before pushing,
  even for a completed version." It now says the opposite: push automatically,
  no confirmation, and do not ask a question at the end. That file is
  gitignored (Session 8 decision), so the change lives only on this machine and
  will not show up in a fresh clone — worth knowing if the behavior ever seems
  surprising.
- Pushed v0.6's commit and annotated tag, which had been sitting local-only
  from the previous `/end` run under the old ask-first policy.
- No code changed in this entry. 51 tests still passing, tree clean.

**What broke / what to watch:**

- Nothing broke. One thing to be aware of going forward: `/end` now pushes
  whatever is committed, including WIP commits, without asking. That is the
  requested behavior, but it means anything staged at the end of a session goes
  to GitHub.

**Next session should:**

- Pick the 8th version — see Next Up. v0.7 (scaled scoring) is the small
  unblocked one; v0.8 (deploy) is the one that makes the project actually
  usable by its intended audience.

**Reconstruction prompt (only if this session completed a version):**

```
Not applicable — process/docs only. v0.6's reconstruction prompt is in the
Session 11 entry below and was written when that version completed.
```

---

### [v0.6] Session 11 — 2026-08-11 (full-length timed practice test)

> Continued directly from Session 10 in the same working session — the entries
> are split by version, per this log's convention, not by wall-clock session.

**Prompt(s) used:**

```
if everything is good for v0.5 please continue to v0.6 after pushing,
tagging and logging
[plan mode; two scoping decisions via AskUserQuestion: configurable section
sizes shipping reduced, and a hard cutoff with in-memory state]
```

**What was done:**

- Pushed and tagged v0.5 first, then planned v0.6.
- **Surfaced the content gap before designing anything.** The real blueprint
  needs ~50 LR and ~27 RC across 4 passages; the bank has 42 LR and 10 RC
  across 2. A blueprint-accurate test would serve every RC question 2.7 times.
  The user chose configurable section sizes: ship reduced (21/21/10) with
  nothing repeated, keep a `blueprint` preset that refuses with a countable
  shortfall, and state the gap on the start screen.
- Built `app/assembly.py`, `GET /api/test/new`, `POST /api/test/grade`, a
  `useCountdown` hook, and the `/test` page (start / section runner / break /
  results), plus `tests/test_assembly.py` (15 tests, 51 total).
- Reused rather than rebuilt: `_row_to_public` for no-leak serialization,
  `insert_attempt` so tests feed `/progress`, `QuestionCard` and
  `GradeResultView` from v0.3, and the existing theme classes. No new CSS.

**What broke / what to watch:**

- **`useCountdown` ended each section the instant it began.** The ordinary
  useState+useEffect shape returns a stale 0 on the first render after a new
  deadline is set, and the caller treats 0 as "time is up". Fixed by deriving
  the value during render; the hook carries a comment saying not to simplify it
  back. **The unit tests would never have caught this** — it took driving the
  real page in a browser.
- Two smaller self-inflicted issues: pytest tried to collect `TestAssemblyError`
  as a test class (renamed the module to `app/assembly.py` and the exception to
  `AssemblyError`), and `assemble_test(seed=...)` wasn't actually reproducible
  because `get_questions_filtered` returns rows `ORDER BY RANDOM()` — the rows
  are now sorted before the seeded shuffle.
- Playwright's `clock.install()` / `fastForward()` is what made testing a
  35-minute timer practical. Worth reaching for again.

**Next session should:**

- Pick the 8th version. v0.7 (scaled 120-180 scoring) is unblocked and small now
  that v0.6 produces a raw score to convert. v0.8 (deploy) is the last core
  feature and the actual point of the project — the friend cannot use
  localhost. RC content expansion would additionally unlock v0.6's blueprint
  preset.

**Reconstruction prompt — v0.6 (full-length timed practice test):**

```
Rebuild this project (LSAT Prep) to v0.6's state. Everything in the v0.1, v0.2,
v0.3 and v0.5 reconstruction prompts, PLUS a full-length timed practice test.

SCOPE NOTE — READ FIRST: the real LSAT is 2 LR sections of 24-26 plus an RC
section of 26-28 across 4 passages. The bank holds 42 LR and 10 RC across 2
passages, so a blueprint-accurate test is impossible without serving RC
questions ~2.7 times each. This version ships REDUCED section sizes and says so
in the UI. Do not "fix" this by allowing repeats.

app/assembly.py:
- SectionSpec(kind, label, question_count, minutes=35); kind is
  "logical_reasoning" or "reading_comprehension".
- PRESETS: "reduced" = LR 21 / LR 21 / RC 10 (sized so nothing repeats);
  "blueprint" = LR 25 / LR 25 / RC 27 (the real thing).
- AssemblyError for insufficient content. Do NOT name it TestAssemblyError —
  pytest tries to collect any class starting with "Test", and for the same
  reason this module must not be named app/test_assembly.py.
- assemble_test(conn, preset, seed=None):
  * NO QUESTION APPEARS TWICE anywhere in the paper. Draw LR without
    replacement across ALL LR sections, not per section. This is the invariant
    the tests pin.
  * Spread LR across question_type by round-robin rather than taking a random
    draw, so a section isn't one type repeated.
  * Assemble RC BY WHOLE PASSAGE, never by sampling N questions: a passage is
    read once and answered against several times, and independent sampling
    strands questions whose passage the test never shows.
  * Errors must NAME THE SHORTFALL ("need 50, have 42 (short by 8)") — that is
    what keeps "blueprint" honest instead of silently serving a half-test.
  * get_questions_filtered returns rows ORDER BY RANDOM(), so sort by id before
    the seeded shuffle or `seed` won't actually reproduce anything.
- content_warnings(conn): plain statements of where the bank falls short, for
  the UI to display.

API (reuse _row_to_public so the no-leak guarantee stays in one place):
- GET /api/test/new?preset=reduced -> {preset, sections:[{kind,label,minutes,
  passages,questions}], warnings:[...]}. No correct_answer, no explanation.
  400 with the shortfall message when the bank can't fill the preset.
- POST /api/test/grade -> {answers:[{question_id, selected_answer|null}]}.
  Returns per-question results plus total/correct/answered. A BLANK IS SCORED
  INCORRECT but logs NO attempt row — the real LSAT has no guessing penalty,
  but a blank is still wrong, and logging a non-attempt would distort
  /progress's accuracy-by-type. Answered questions DO log an attempt.

FRONTEND — app/_components/Timer.tsx:
- useCountdown(deadline) driven by a deadline TIMESTAMP, not a decrementing
  counter: a backgrounded tab throttles intervals and a counter would hand back
  time the taker didn't have.
- CRITICAL: it must recompute DURING RENDER when the deadline changes, not only
  in an effect. The plain useState+useEffect version returns a stale 0 on the
  first render after a new deadline is set, and a caller that reads 0 as "time
  is up" ends the section the instant it starts. This bug is invisible to unit
  tests — it only shows up driving the real page.

FRONTEND — app/test/page.tsx, phases idle / running / break / grading / results:
- Fetch the paper on MOUNT so the start screen can state the content gap before
  the test begins; "Start Test" only sets the deadline and flips the phase.
- Start screen lists the sections and says plainly that the test is reduced,
  that each section auto-ends, and that a reload loses everything.
- Section runner: hard cutoff at 0:00 auto-submits and advances with no
  confirmation. Free Previous/Next within a section. Answer state is a
  {questionId: letter} map. Reuse QuestionCard with no result so nothing is
  marked right or wrong mid-test. In the RC section, pin the passage beside the
  question the way /reading-comp does.
- Results: raw score, per-section counts, and per-question review reusing
  GradeResultView. Say that scaled 120-180 scoring is v0.7.
- Add a "Practice Test" nav link. No new CSS — reuse existing theme classes.

TESTING: browser-verify with Playwright's clock.install() + fastForward() —
that is what makes a 35-minute timer testable. Confirm each section
auto-advances on expiry with no click.

NOT YET IMPLEMENTED as of v0.6: scaled 120-180 scoring (v0.7 — v0.6 reports raw
counts only); deployment (v0.8); resuming an interrupted test; RC content
expansion (which would unlock the blueprint preset). The live Anthropic
generate/verify pipeline still exists and has still never been run.
```

---

### [v0.5] Session 10 — 2026-08-10 (near-duplicate detection)

**Prompt(s) used:**

```
lets move onto v0.5
[plan mode; two scoping decisions via AskUserQuestion: authoring-time check
over the existing bank rather than a runtime gate on generation, and local
embeddings rather than a hosted API]
```

**What was done:**

- **Rescoped v0.5 before building.** Its stated job was gating generated
  questions for uniqueness, but the app has no runtime generation — the live
  pipeline has still never been run — so a runtime gate would be infrastructure
  with no traffic. The bank itself is unmeasured, and v0.3 had already found
  near-duplicates in it, so the user chose an authoring-time check.
- **Confirmed Anthropic has no embeddings endpoint** by loading the `claude-api`
  skill rather than answering from memory. That made "embeddings" mean either a
  second vendor or a local model; the user chose local.
- Built `app/similarity.py` (text selection, sha256 content hashing, cosine
  matrix, pair ranking, lazy model load), an `embeddings` cache table in
  `db.py`, `scripts/check_duplicates.py`, and `tests/test_similarity.py`
  (14 tests). 36 tests total.
- **Kept PyTorch out of the critical path.** `sentence-transformers` is an
  optional `dedup` extra; numpy is core. Verified `uv run pytest` passes with
  torch not installed. The venv goes from ~90MB to 790MB *with* the extra —
  which is why it is not a core dependency.

**What broke / what to watch:**

- **The version does not do the thing that motivated it, and this is measured,
  not suspected.** The LR 0/14/15 cluster ranks 79th, 216th and 382nd of 861 LR
  pairs (0.673 / 0.623 / 0.579), well below the 0.80 threshold. No threshold
  fixes it: those questions differ genuinely in topic and wording, and that is
  all cosine similarity measures. Their duplication is architectural. Logged to
  Backlog with the numbers rather than declared a success.
- **Two silent-failure bugs found and fixed mid-build.** Embedding the RC
  passage made every question sharing a passage score *exactly 1.000* — the
  ~555-token passage both dwarfs the ~60-token stem and overflows
  all-MiniLM-L6-v2's 256-token limit, so the embedded text was the first 256
  tokens of the passage and the stems never reached the model at all. Separately,
  the bank's longest question (271 tokens) exceeded that same limit. Fixed by
  not embedding passages, moving to a 512-token model, and making `embed()`
  raise on over-length input instead of truncating quietly.
- The first fix was caught only because the scores were suspiciously *exactly*
  1.000. Worth remembering: an embedding pipeline fails silently by default.

**Next session should:**

- Decide on the structural tell checker (Backlog) — it is the piece that
  actually addresses the memorizability requirement, and it is small.
- Or scope v0.6, noting the RC content shortfall against a real blueprint.

**Reconstruction prompt — v0.5 (near-duplicate detection):**

```
Rebuild this project (LSAT Prep) to v0.5's state. Everything in the v0.1, v0.2
and v0.3 reconstruction prompts, PLUS an authoring-time near-duplicate check.
(v0.4's dashboard and v0.9's theme are separate completed versions layered on
top in real project history.)

SCOPE NOTE: v0.5's original Version Plan entry said "uniqueness/dedup check via
vector DB," written when generation was expected to run live. It does not: all
52 questions are hand-authored and the pipeline in app/generation.py has never
been run. So this is an authoring-time report over the bank, NOT a runtime gate,
and NOT a Postgres/pgvector migration.

DEPENDENCIES:
- numpy: core dependency.
- sentence-transformers: an OPTIONAL extra named `dedup`, because it pulls
  PyTorch and takes the venv from ~90MB to ~790MB. The app and the whole test
  suite must run with torch absent — verify this, don't assume it.
  Install for the check with: uv sync --extra dedup

app/similarity.py:
- EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5" (512-token context, 384 dims).
  Do NOT use all-MiniLM-L6-v2: it truncates at 256 tokens and the bank's
  longest question (a parallel-reasoning item whose five choices are each full
  arguments) is 271 tokens, so it would be silently cut.
- question_text(question): stimulus (LR only — RC carries stimulus=None), stem,
  and choices, newline-joined. The RC passage is deliberately EXCLUDED. Two RC
  questions about one passage are intentionally different questions about
  shared material, not duplicates. Including the passage fails twice over: a
  ~555-token passage dwarfs a ~60-token stem, AND it overflows the token limit,
  so the embedded text becomes the first N tokens of the passage and nothing
  else — every question sharing a passage scores exactly 1.000 and the stems
  never reach the model. If you see exactly 1.000, this is why.
- content_hash(text): sha256. Cache key.
- embed(texts): lazy-imports SentenceTransformer inside the function so
  importing this module never pulls torch; raises a clear ImportError naming
  the extra if it is missing. MUST raise ValueError on any text longer than
  model.max_seq_length rather than letting truncation happen silently.
- cosine_matrix(vectors): row-normalize (zero-norms set to 1 so zero vectors
  give 0, not NaN), then V @ V.T.
- rank_pairs(vectors, labels, threshold): upper-triangle pairs only, sorted
  descending. Pure numpy — this is what the tests exercise.

app/db.py — add an `embeddings` table: content_hash TEXT PRIMARY KEY, model
TEXT, vector BLOB, created_at. Keyed by content hash, NOT question_id: the seed
script wipes and reinserts questions with fresh autoincrement ids, so an
id-keyed cache would die on every reseed. get_cached_embeddings(conn, hashes,
model) and store_embedding(...); float32 via .tobytes() / np.frombuffer.
Scope lookups by model so swapping models cannot reuse stale vectors.

scripts/check_duplicates.py — reads the CANONICAL SOURCE FILES
(app.mock_questions.MOCK_QUESTIONS, app.rc_content.RC_QUESTIONS), not the DB.
Embeds only uncached text. Flags: --threshold (default 0.80), --fail-over
(default 0.95, exits 1), --top N. Annotates same-passage RC pairs
"[same passage — expected]" and excludes them from the failure gate — they
score 0.85-0.90 by design and are not duplicates.

tests/test_similarity.py — must NEVER call embed() or import
sentence_transformers; feed hand-built vectors to the pure functions. Cover
identical/orthogonal/zero vectors, magnitude invariance, pair ordering, each
pair once and never self, threshold filtering, that question_text excludes the
passage, and the SQLite BLOB round trip including model scoping.

KNOWN LIMITATION — DO NOT PRESENT THIS AS SOLVED. This catches questions that
converge in TOPIC AND WORDING. It does NOT catch structural duplication. On the
real bank the known LR 0/14/15 near-duplicate cluster ranks 79th, 216th and
382nd of 861 LR pairs (0.673 / 0.623 / 0.579) — far below threshold, and no
threshold fixes it, because those questions are about security cameras, museum
finances and bike-share and are genuinely dissimilar in wording. What makes
them duplicative is answer architecture (each key the only hedged choice, each
trap the only absolute one). That needs a structural fingerprint, which v0.5
does not build.

NOT YET IMPLEMENTED as of v0.5: the structural tell checker described above;
full-length timed test assembly (v0.6 — and note the bank holds 42 LR / 10 RC
against a blueprint needing ~50 LR / ~27 RC); scaled scoring (v0.7); deployment
(v0.8). The live Anthropic generate/verify pipeline still exists and has still
never been run.
```

---

### [v0.3] Session 9 — 2026-08-10 (filtered practice + LR bank expansion)

**Prompt(s) used:**

```
lets continue with v0.3
[plan mode; two scoping decisions made via AskUserQuestion: "mechanism +
bulk authoring" over mechanism-only, and a new dedicated page over
extending the existing Practice page]
```

**What was done:**

- **Found before building** that half of v0.3's stated scope (metadata
  tagging) was already satisfied by v0.1/v0.2, and that the LR bank held
  exactly one question per type — so "cycle through flaw questions" would
  have been a pool of one. Also found `content_area` is NULL on all 24
  question rows; the area lives only on `passages`. Both facts were put to
  the user, who chose to expand the bank alongside the mechanism.
- **Backend:** `get_questions_filtered()` (parameterized `IN` clauses, LEFT
  JOIN to passages, `COALESCE` on content area) and `get_taxonomy_counts()`
  in `db.py`; `GET /api/taxonomy` and `GET /api/questions/filtered` in
  `main.py`, reusing the existing `_row_to_public` so the no-leak guarantee
  is shared rather than reimplemented; four new Pydantic models;
  `tests/test_filtering.py` with 9 tests (22 total, all green).
- **Frontend:** new `app/_components/QuestionCard.tsx` holding the shared
  question card and grade-result view — `/` and `/reading-comp` were
  refactored onto it rather than letting `/focus` triplicate the markup.
  New `app/focus/page.tsx` and a 4th nav tab.
- **Content:** authored 28 new LR questions to bring all 14 types to 3 each.
- **Verification, three rounds.** 31 questions (28 new + the 3 originals that
  had never been independently checked) through a blind re-solve: 31/31
  agreed. Then an adversarial distractor pass on all 31, which is what found
  the real defects. After the resulting edits, 19 touched questions were
  re-solved blind again: 19/19 still agreed.
- **Defects found and fixed** — see Current State for the full list; the
  most serious were a double-key inference item, a sufficient-assumption
  stimulus missing the premise its key depended on, and an
  evaluate-the-argument premise that granted half its own answer.
- **Two bank-level tells fixed:** answer-letter skew (B was 57% of keys) and
  an answer-length tell where the key was the longest choice 76% of the time
  against a ~20% baseline. The latter predated this version and affected
  v0.1's questions too.
- Documented the two-pass protocol and the bank-level tell checklist in
  `.claude/skills/lsat-methodology/SKILL.md`; updated `CLAUDE.md` structure
  and routes; regenerated `prep.txt` (52 questions, 1548 lines).

**What broke / what to watch:**

- Two self-inflicted mechanical errors, both caught immediately: a
  `sed`-style replacement left a dangling string fragment in one stimulus,
  and a single-quoted literal broke on an apostrophe in "Ridgeline
  Elementary's". Both are the predictable hazard of scripted edits to a
  Python source file holding prose — prefer block-scoped, exact-match
  rewrites and always re-import afterwards.
- Batched verification (6 agents x ~6 questions) rather than one agent per
  question as the plan estimated. Key-blindness is preserved, so the check
  is equally valid, at roughly a fifth of the cost.
- **Still open, logged to Backlog:** roughly a third of items were rated
  "too_easy" by the adversarial pass, with concrete per-item rewrite
  suggestions; the residual length tell; and the fact that
  `MOCK_QUESTIONS[2]` is verbatim the skill's reference example, which makes
  it both memorizable and impossible to verify independently.

**Next session should:**

- Decide what gets built 6th. v0.6 (full-length timed test) is now unblocked
  — v0.3 supplied the type/content-area selection it needs — and is the
  user's oldest outstanding request.
- Or spend a focused session on the question-quality Backlog items, which
  now have specific, itemized fixes rather than vague concerns.

**Reconstruction prompt — v0.3 (filtered practice mode + LR bank expansion):**

```
Rebuild this project (LSAT Prep) to v0.3's state. This is everything in the
v0.1 and v0.2 reconstruction prompts, PLUS the following. (v0.4's dashboard
and v0.9's theme are separate completed versions layered on top in real
project history; this entry describes v0.3's own logical scope.)

BACKEND - FILTERING:
- db.py gains get_questions_filtered(conn, section=None, question_types=None,
  content_areas=None) returning all matching rows ORDER BY RANDOM(). It must
  LEFT JOIN passages ON questions.passage_id = passages.id and filter content
  area on COALESCE(q.content_area, p.content_area) - RC questions store NULL
  for content_area, so without the join a content-area filter returns nothing.
  Build IN (...) clauses from parameterized placeholders; never interpolate
  values into SQL.
- db.py gains get_taxonomy_counts(conn) -> (type_rows, content_area_rows).
  Group types by (section, question_type). Group content areas by the same
  COALESCE expression, excluding NULLs, and GROUP BY 1 / ORDER BY 1 by
  ordinal - a bare `content_area` is ambiguous because both joined tables
  have a column with that name, and SQLite raises OperationalError.
- GET /api/taxonomy -> {types: [{section, question_type, count}],
  content_areas: [{content_area, count}]}. The UI builds its filter controls
  from this so options cannot drift from the bank's actual contents.
- GET /api/questions/filtered?section=&question_type=&content_area= ->
  {total, questions: [...]}. question_type and content_area are repeatable
  (FastAPI: list[str] | None = Query(None)) for multi-select. Returns the
  WHOLE matching set at once in random order, so the frontend can cycle it
  without repeats - a different shape from LR's one-question-per-call draw.
  A filter combination matching nothing returns 200 with total=0, NOT 404;
  an empty result is a valid answer the page must render as "no questions
  match", not an error. Reuse the existing _row_to_public helper so the
  never-leak-the-key guarantee is shared, not reimplemented.
- Note /api/questions/... (plural) does not collide with the existing
  /api/question/{question_id}.
- tests/test_filtering.py: empty-state taxonomy, taxonomy counts, filter by
  one type, by several types, by section, by RC content area through the
  passage join, no-filters-returns-all, unknown type -> empty set with 200,
  and that filtered results never include correct_answer or explanation.

FRONTEND:
- app/_components/QuestionCard.tsx (the _folder prefix is Next 16's
  private-folder convention for colocated non-routable UI). Exports the
  Question and GradeResult types, LETTERS, formatQuestionType(), a
  QuestionCard component (stimulus when present, stem, radio choices, all
  inside .clean-card) and a GradeResultView component (.result-chip plus the
  explanation in a .clean-card). Presentational only - each page keeps its
  own state and grading fetch, because the three flows genuinely differ.
- app/page.tsx and app/reading-comp/page.tsx are refactored onto these
  components with identical rendered output; do not let the new page
  triplicate the markup.
- app/focus/page.tsx: fetches /api/taxonomy on mount, groups types by section,
  renders checkbox groups with counts inside .wood-panel blocks plus a
  content-area group, then "Start Session" fetches the filtered set. Cycles
  one question at a time with a "Question N of M - Type: X" indicator,
  ending in a "Session complete / N of M correct" panel and a "New Session"
  button. Empty result renders "No questions match those filters" with a
  "Change Filters" button. No new CSS - reuse v0.9's existing classes.
- layout.tsx gains a 4th nav link, "Focus" -> /focus.

CONTENT - LR BANK EXPANSION:
- Expand mock_questions.py from 14 to 42 questions: exactly 3 for each of the
  14 official LR types. Without this, filtering to a single type returns a
  pool of one and the whole feature is pointless.
- Every question carries a full methodology-based explanation that applies
  the named method for its type and addresses all five choices.

VERIFICATION PROTOCOL - TWO PASSES (this is the important part):
1. Independent re-solve: a fresh context sees only stimulus/stem/choices/type,
   never the key, and solves using the named method. Keep only on match.
2. Adversarial distractor pass: a second fresh context argues the strongest
   case FOR each wrong answer, then judges whether any is genuinely defensible
   (= two correct answers) and whether all four are trivially dismissible
   (= item too easy).
Pass 1 alone is not sufficient and will report 100% agreement on a bank that
still contains double-key items and unusable distractors. Pass 2 is what
found, in this version: an inference item where an exclusive disjunction made
a "wrong" answer strictly derivable; a sufficient-assumption stimulus that
never established its subject belonged to the class its rule quantified over;
and an evaluate-the-argument premise that granted half of its own key.

BANK-LEVEL TELLS - MEASURE THESE, THEY ARE INVISIBLE PER QUESTION:
- Answer-letter distribution must be roughly uniform. This bank reached
  B = 24/42 (57%) before rebalancing to A=9 B=8 C=10 D=8 E=7. Rebalance by
  swapping two choices and swapping the corresponding "(X)"/"(Y)" references
  inside the explanation - a swap keeps the other three letters stable, and
  scoping the regex to parenthesized letters leaves bare logic variables
  ("let A = artifacts") untouched.
- The correct answer must not systematically be the longest choice. Baseline
  is ~20%; this bank measured 76%, meaning a student could score most of it
  by picking the longest option without reading the stimulus. Fix by trimming
  over-elaborated keys and padding thin distractors.
- Per-type answer architecture must vary. All three necessary-assumption keys
  were once the only hedged choice while the trap was the only absolute one,
  so "pick the hedged one" scored 3/3 without any negation test.

DOCS: record the two-pass protocol and the tell checklist in
.claude/skills/lsat-methodology/SKILL.md. Regenerate prep.txt.

NOT YET IMPLEMENTED as of v0.3: dedup/uniqueness via vector DB (v0.5);
full-length timed test assembly (v0.6 - now unblocked, since v0.3 supplies
the type/content-area selection it needs); scaled scoring (v0.7); deployment
(v0.8). RC content is still only 2 passages (law, natural_science) and 8 of
10 rc_ types. The live Anthropic generate/verify pipeline still exists and
has still never been run. Known open quality debt: about a third of items
have distractors rated too easy, a residual answer-length tell, and
MOCK_QUESTIONS[2] is verbatim the methodology skill's reference example,
which makes it memorizable and impossible to verify independently.
```

---

### [v0.2 + docs] Session 8 — 2026-08-09 (build-order audit, date fixes, v0.2 finalized)

**Prompt(s) used:**

```
[/resume]

Before I approve v0.2, I need to understand the actual build order. The
frontend reused "v0.9 theme classes" for the RC page, which implies theme
(v0.9) was already built before v0.2 (RC) — but the Version Plan lists v0.2
before v0.9. What's the true chronological build order so far, version by
version? And does the Version Plan table's numbering still represent the
order things were/will be built in, or has it drifted from that? If it's
drifted, fix the table now so it accurately reflects reality before we go
any further — I'd rather have honest numbering than a table that looks
sequential but isn't.

continue and fix this. Once all the bugs and mismatches are fixed, lets
continue with v0.2
```

**What was done:**

- **Build-order audit.** The user's inference was correct: v0.9 was completed
  and tagged before v0.2 was started. Reconstructed the true order from `git
  log`/`git for-each-ref` rather than from the session narrative. Write order:
  v0.1 (Session 1 base app) → v0.4 → v0.9 (both Session 2) → v0.2 (Session 6).
  Completion order: v0.4 and v0.9 together (`6725b0b`, 18:35) → v0.1
  (`7f6cbd3`, 19:06) → v0.2. Cause of the drift: v0.4/v0.9 were explicitly
  authorized to proceed while v0.1 sat blocked on an API key, and v0.1 then
  completed by having its scope revised rather than by the blocker clearing.
- Added a **Build order column** to the Version Plan giving each version both
  its write position and its completion position, with tag + commit hash for
  the done ones and an explicit "order undecided" for the rest (plus v0.6's
  hard dependency on v0.3, and a note that v0.8 sits *before* an
  already-finished v0.9). Added a header note stating the numbers are stable
  scope IDs. **Renumbering was considered and rejected** — `v0.1`/`v0.4`/`v0.9`
  are annotated tags already pushed to GitHub and every reconstruction prompt
  cross-references those numbers, so renaming would damage published history
  to fix a presentation problem. Mirrored a one-line version of this into
  `README.md` and added a Key Decisions row.
- **Date correction.** Sessions 4-7, eight Key Decisions rows, the
  Reconstruction Prompts Index, and two Version Plan scope cells all claimed
  `2026-08-10`; every commit in the repo is dated `2026-08-09`. Root cause
  found rather than guessed: `prep.txt`'s generated header reads
  `2026-08-10T02:36:54+00:00`, which is **UTC** — 19:36 PDT on 08-09 — and got
  copied in as a local date. Corrected all of them in `prompt.md` and logged
  the correction itself as a Key Decisions row so the rewrite isn't silent.
  `prep.txt` deliberately NOT changed: it's a derived export and its UTC
  timestamp is correct.
- **Independent re-verification of v0.2** instead of trusting Session 6's
  screenshots (which this session could not see): 13/13 pytest; in-process
  bank integrity check (14 LR / 14 unique types, 2 passages, 10 RC / 8 types,
  zero missing explanations, all 5-choice with valid A-E keys); live uvicorn
  smoke test on port 8077 covering the passage endpoint's shape and
  non-leakage, all five answer letters against RC question 39, and 12 LR draws
  confirming `passage_id IS NULL` separation holds; `tsc --noEmit` and
  `npm run build` both clean. Confirmed `prep.txt` regenerates identically
  apart from its timestamp.
- Updated `CLAUDE.md`'s Commands section — the "Build: not configured yet (no
  production build has been run for either side)" line was stale the moment
  the build above succeeded.
- Fixed the **stale Next Up section**, which was still listing "get
  confirmation on the v0.1 checklist, then tag v0.1" long after v0.1 shipped.

**What broke / what to watch:**

- **Two genuine bugs found, neither fixed, both logged to Backlog** — both are
  pre-existing v0.4 defects, not v0.2 regressions, and fixing them inside v0.2
  would violate the Versioning Strategy:
  1. Orphaned `attempts` rows. The seed script wipes and reinserts `questions`
     with fresh ids but never clears `attempts`, and the FK has no
     `ON DELETE CASCADE` (sqlite3 also doesn't enforce FKs without
     `PRAGMA foreign_keys = ON`). Reproduced live: `/api/stats/summary`
     reported overall total 7 while the by-type rows summed to 5. Session 5
     noted this in passing; this session confirmed it still reproduces.
  2. `/progress`'s "attempts over time" buckets by **UTC** date, so US-Pacific
     evening practice charts on the following day. Same root cause as the log
     date confusion above.
- v0.2's code was not modified this session — only docs. The re-verification
  was read-only apart from reseeding the gitignored local dev DB.

**Next session should:**

- Build v0.3 (filtered/cycle-by-type practice) — recommended 5th, since it's
  small, unblocked, and a hard prerequisite for v0.6's timed full test.
- Consider knocking out the two Backlog bugs above as a quick standalone fix
  first; they're both small and they make `/progress` actively misleading.

**Reconstruction prompt (only if this session completed a version):**

```
Not written separately — this session finalized v0.2, whose reconstruction
prompt was already drafted in the Session 6 entry below and needed no
changes (no v0.2 code was modified this session). It is now listed in the
Reconstruction Prompts Index as the 4th completed version.
```

---

### [v0.2] Session 7 — 2026-08-09 (session wrap-up / handoff)

**Prompt(s) used:**

```
add to the prep.txt the reasoning of why an answer is the right answer.
also add this to CLAUDE.md so it is always done after every new question
is created

Before I restart this session, save state now using the /end logic even
though the shortcut may not be working: 1) update prompt.md's Current
State (overwrite), 2) add a new Session Log entry (prompts, what was
built/changed, what broke/unverified, next-session instructions), 3)
check whether the current version is genuinely complete end-to-end -
this sounds like it's still in progress based on what we were just doing
(testing RC submit->grade->next-question) - if so, commit as WIP with a
clear message, don't check off README, don't write a reconstruction
prompt, don't tag, unless actually fully done, 4) print a short summary
(version/status, what got done, what's next, pushed vs. local-only).
Then confirm you're done before I restart.
```

**What was done:**

- Checked `prep.txt`: the reasoning was already present for all 24
  questions (`Correct Answer:` + full `Explanation:` per entry, pulled
  from the `explanation` field every question already requires). Nothing
  needed adding to the file itself. Strengthened `CLAUDE.md`'s Workflow
  Notes rule to say this explicitly — the `explanation` field must contain
  full methodology-based reasoning, and `prep.txt` inherits it
  automatically via the export script — so it's an unambiguous, documented
  requirement going forward, not just an implicit side effect of how the
  script happens to work today.
- **Corrected the record on v0.2's status.** The user's guess that the RC
  flow was "still in progress" wasn't quite accurate — that flow (submit →
  grade → next-question) was actually tested successfully via Playwright
  earlier this session (Session 6), with screenshots confirming it works.
  What was genuinely missing was the user's *explicit confirmation* of the
  Session 6 finishing-checklist, which was presented but never answered
  (the conversation moved to the `prep.txt` question instead). Per the
  user's own instruction this turn ("unless actually fully done"), and
  since that confirmation gate was never cleared, v0.2 is being treated as
  NOT done: reverted `README.md`'s v0.2 checkbox back to unchecked, reverted
  the Version Plan status from "DONE" to "built + verified, pending
  confirmation," and removed the v0.2 row from the Reconstruction Prompts
  Index (the reconstruction prompt text itself stays drafted in the
  Session 6 entry, ready to reuse once confirmed — no need to rewrite it).
- Overwrote `prompt.md`'s Current State to reflect this precisely.
- Committed everything (v0.2's RC feature + `prep.txt` tooling + this
  session's doc corrections) as a single **work-in-progress commit** — no
  annotated tag, not pushed to GitHub. See commit hash in the summary
  printed after this entry / in `git log`.

**What broke / what to watch:**

- Nothing code-level broke this session — this was verification-status
  bookkeeping and a documentation clarification, not new feature work.
- The untracked `.claude/commands/resume.md` file (noted in Sessions 5-6)
  is still sitting there, still not staged into any commit — it's IDE/
  harness-created, not this project's work, so it's being left alone
  again.
- Because v0.2 is committed as WIP rather than finished, `main`'s latest
  commit will NOT be tagged `v0.2` — don't assume the presence of a commit
  means the version is "done" per this project's own definition; check
  `prompt.md`'s Current State and the Version Plan status column instead.

**Next session should:**

- Ask the user directly: "Does v0.2 (2-passage RC) look good to finalize?"
  If yes: re-check the README box, add the v0.2 row back to the
  Reconstruction Prompts Index (prompt text already exists in Session 6),
  amend the Version Plan status to DONE, then commit that (or amend into
  the existing WIP commit if it hasn't been pushed anywhere else yet),
  annotated-tag `v0.2`, and push everything (this WIP commit has not been
  pushed, so v0.1/v0.4/v0.9's tags are the only ones currently on GitHub).
- If the user wants changes to v0.2 first, make them, then re-run the
  verification/confirmation cycle before tagging.
- Separately, decide next priority per the last few sessions' open
  question: v0.3 (filtered/cycle-by-type) vs. expanding RC content
  (Backlog) vs. scoping v0.6 (timed test).

**Reconstruction prompt (only if this session completed a version):**

```
Not written — this session did not complete a version. (v0.2's
reconstruction prompt was already drafted in the Session 6 entry below,
in preparation for when it IS confirmed; it does not need to be rewritten,
just reused once the user confirms and the version is actually tagged.)
```

---

### [v0.2] Session 6 — 2026-08-09

**Prompt(s) used:**

```
lets work on v0.2 instead
[proposed data model (passages table + passage_id FK), a 10-type RC
taxonomy, and a 4-passage/20-question content plan (law, natural_science,
social_science, humanities x 5 each) before building]

Lets start smaller. Then once done. Create a txt file with all of the
questions and answers called prep.txt
#Whenever you create a new question and answer, add it to the prep.txt
```

**What was done:**

- Reduced v0.2's starting scope to 2 passages (law, natural_science) per
  the user's "start smaller" direction, instead of the originally proposed
  4.
- Defined a 10-type RC question taxonomy (rc_main_point,
  rc_specific_detail, rc_inference, rc_author_attitude,
  rc_passage_organization, rc_analogous_situation, rc_application,
  rc_strengthen_weaken, rc_purpose_of_reference, rc_meaning_in_context) and
  added it to the `lsat-methodology` skill, alongside the existing LR
  taxonomy.
- Data model: added a `passages` table (content_area, title, passage_text)
  and a nullable `passage_id` FK on `questions`; made `stimulus` nullable
  (RC questions have none of their own). Deleted and recreated the local
  dev DB to pick up the new schema (gitignored, disposable).
- Authored 2 original passages (~460-470 words each) and 5 questions per
  passage (10 total), covering 8 of the 10 RC types. **Independently
  verified all 10** the same way as v0.1's LR questions — 10 parallel fresh
  subagents, each given only the passage + question + choices (never the
  marked answer). 10/10 matched on the first pass.
- Backend: `GET /api/passage/random` (returns one random passage + ALL of
  its questions together, so the frontend can keep the passage pinned
  while cycling — different shape than LR's one-question-at-a-time random
  draw). `get_random_question()` (LR) updated to explicitly exclude
  passage-attached rows (`WHERE passage_id IS NULL`) so the two flows stay
  separate. Grading needed zero changes — the existing
  `POST /api/question/{id}/grade` already worked generically for any
  question by id. Updated `scripts/generate_question.py` to also seed
  passages + RC questions in mock mode. Added `tests/test_reading_comp.py`
  (4 tests: 404 on empty, passage+questions returned correctly with
  answer/explanation never leaked, RC grading works, LR's random endpoint
  excludes RC questions) — 13/13 backend tests passing.
- Frontend: new `/reading-comp` nav tab and page. Passage stays pinned in a
  `.clean-card` (scrollable) on the left while the user cycles through its
  5 questions one at a time on the right (`Question N of 5` indicator);
  "Next Question" advances within the same passage, "New Passage" appears
  only after the last question and fetches a new random passage. Reused
  the existing `.block-btn`/`.result-chip`/`.clean-card` theme classes
  as-is — no new CSS needed. Visually confirmed via Playwright: initial
  passage+question render, full submit → grade → "Correct!" chip →
  explanation → "Next Question" → question 2 loads with a fresh radio
  selection.
- Built `scripts/export_prep_txt.py`, which regenerates `prep.txt` (repo
  root) from the canonical source files (`mock_questions.py`,
  `rc_content.py`) — 14 LR questions + 2 passages/10 RC questions, ~710
  lines, human-readable. Added a standing rule to `CLAUDE.md`'s Workflow
  Notes: regenerate `prep.txt` after authoring any new question, never
  hand-edit it directly (also noted in Do NOT touch). Updated `CLAUDE.md`'s
  Project Structure and Commands sections to reflect the new files.
- Per `CLAUDE.md`'s Finishing a Version checklist, did NOT commit, tag, or
  push yet — presenting the checklist next, for user confirmation.

**What broke / what to watch:**

- Had to delete the local `backend/data/lsat_prep.db` file to pick up the
  new `passages` table / `passage_id` column, since the schema uses
  `CREATE TABLE IF NOT EXISTS` (won't alter an existing table). This file
  is gitignored/disposable, so this was safe, but worth remembering if the
  schema changes again — it doesn't auto-migrate.
- v0.2 is being marked done at a deliberately reduced scope (2 of the
  originally-proposed 4 content areas, 8 of 10 RC types). This mirrors how
  v0.1 was completed at a revised/reduced scope earlier this session — see
  the new Backlog entry for expanding RC content later.
- The untracked `.claude/commands/resume.md` file (noted in Session 5) is
  still sitting there, still not part of this session's work, still not
  staged into any commit.

**Next session should:**

- Get user confirmation on this checklist, then commit + tag `v0.2` + push.
- Decide next priority: v0.3 (filtered/cycle-by-type practice, small) vs.
  expanding RC content (Backlog) vs. scoping v0.6 (timed full test) now
  that both LR and RC exist, even at reduced scope.

**Reconstruction prompt — v0.2 (Reading Comprehension, reduced starter scope):**

```
Rebuild this project (LSAT Prep) to v0.2's state. This is everything in the
v0.1 reconstruction prompt (Session 5, above) PLUS the following Reading
Comprehension layer. (v0.4's dashboard and v0.9's theme are separate,
already-completed versions layered on top in real project history - this
entry describes v0.2's own logical scope, RC only.)

DATA MODEL ADDITIONS:
- New SQLite `passages` table: id, content_area (TEXT, e.g. "law" or
  "natural_science"), title (TEXT, nullable), passage_text (TEXT), created_at.
- `questions` table gains a nullable `passage_id INTEGER REFERENCES
  passages(id)` column. `stimulus` becomes nullable (NULL for RC questions -
  their text lives on the joined passage instead).
- A passage is read once and has MULTIPLE questions asked against it -
  this is structurally different from LR, where every question is fully
  self-contained.

CONTENT (hand-authored, independently verified - same method as v0.1, no
live API at any point):
- 2 original passages, ~460-470 words each: one law-content-area passage
  (the historical shift from caveat emptor/privity doctrine to strict
  products liability), one natural_science-content-area passage (the
  scientific debate over whether dinosaurs were ectothermic, endothermic,
  or mesothermic).
- 5 questions per passage (10 total), covering 8 of a newly-defined
  10-type RC taxonomy: rc_main_point, rc_specific_detail,
  rc_purpose_of_reference, rc_strengthen_weaken, rc_meaning_in_context
  (law passage); rc_main_point, rc_specific_detail, rc_inference,
  rc_application, rc_author_attitude (natural_science passage). NOT yet
  covered: rc_passage_organization, rc_analogous_situation (Backlog).
- Verification: each question independently re-solved by a fresh subagent
  given only the passage + question + choices (never the marked answer).
  10/10 matched on first pass, zero revisions needed.
- RC question types are prefixed `rc_` even where conceptually close to an
  LR type name (e.g. rc_main_point vs. LR's main_point) - this is
  deliberate, to keep LR and RC fully distinct in the schema and in the
  /progress dashboard's accuracy-by-type breakdown without needing to
  touch that already-shipped stats query.

API:
- `GET /api/passage/random` - returns one random passage PLUS all of its
  associated questions together (not one question at a time): {passage:
  {id, content_area, title, passage_text}, questions: [{id, section,
  question_type, content_area, passage_id, stimulus (null), question_stem,
  choices}, ...]} - no correct_answer/explanation, same privacy pattern as
  the LR endpoint.
- `GET /api/question/current` (LR) updated: `WHERE passage_id IS NULL`
  added to its random-selection query, so it never accidentally serves an
  RC question.
- `POST /api/question/{id}/grade` needed NO changes - it already worked
  generically by question id for any section.
- Seeding script (`scripts/generate_question.py`, mock mode) now also
  inserts the 2 passages and 10 RC questions, mapping each RC question's
  passage_id (a string key in the source data) to the passage's actual
  integer DB id after insert.

FRONTEND:
- New nav link "Reading Comp" -> `/reading-comp`.
- New page: fetches `GET /api/passage/random` once on load. Renders the
  passage in a `.clean-card` (scrollable, pinned) alongside the current
  question (also `.clean-card`, radio choices, "Question N of M · Type: X"
  indicator). Submitting grades via the existing per-question grade
  endpoint and shows the same `.result-chip` + explanation pattern as LR.
  "Next Question" (primary button) advances to the next question ON THE
  SAME PASSAGE, resetting selection/result state; only once the last
  question in the set is answered does the button become "New Passage"
  (secondary button), which re-fetches a new random passage from scratch.
  No new CSS/theme classes were needed - reused v0.9's existing
  `.block-btn`/`.result-chip`/`.clean-card` classes as-is.

TOOLING:
- `scripts/export_prep_txt.py`: regenerates `prep.txt` (repo root, plain
  text) from `mock_questions.py` + `rc_content.py` (the canonical source
  files) - LR questions numbered [1]..[14], then RC organized by passage
  with questions numbered [Q1]..[Q5] per passage. Never hand-edit
  `prep.txt`; re-run this script after authoring/changing any question.
  Standing rule (CLAUDE.md Workflow Notes): do this every time a new
  question is authored and verified.

KEY DECISIONS:
- Started at 2 passages instead of the originally-proposed 4 (user chose
  "start smaller" to validate the approach before a bigger authoring
  commitment) - the other 2 real-LSAT RC content areas (social_science,
  humanities) and the 2 uncovered RC types are logged to Backlog, not
  abandoned.
- RC's practice flow is deliberately a SEPARATE page/flow from LR's, not
  merged into one "random question" endpoint - reading a passage once and
  answering several questions in sequence is fundamentally different UX
  from LR's independent per-question random draw.

NOT YET IMPLEMENTED as of v0.2: same list as v0.1's reconstruction prompt
(filtered/cycle-by-type practice [v0.3], dedup [v0.5], full-length
timed-test assembly [v0.6] - now closer since both LR and RC content
exist, but still needs v0.3 first for type/content-area filtering - scaled
scoring [v0.7], deployment [v0.8]), PLUS: RC content areas social_science
and humanities, and RC types rc_passage_organization / rc_analogous_situation
(all logged to Backlog, not built this version).
```

---

### [v0.1] Session 5 — 2026-08-09

**Prompt(s) used:**

```
Lets work on v0.1. Instead of using AI to generate the questions, lets get
a set of verified used Questions and store the answers and reasoning. Lets
include multiple questions accross different types of questions seen on
the LSAT. I want to work on constructing the foundation algorithm to start
this project
[clarified across 2 rounds: not real/copyrighted LSAT questions (flagged
copyright risk) - original, hand-verified questions, generated without the
Anthropic API]

Lets go with option 1 for now
[Option 1 = Claude hand-authors + independently verifies via fresh
subagent, no live API]

I am testing it and it is only repeating the same question. I need
multiple questions under each type of question that can be seen on the
LSAT with the correct answer and reasoning: [pasted the role_of_statement
question, which was being served on every request]

It works and there are multiple LSAT Prep questions per type. Finish v0.1
and then give me a way to shuffle through all types, cycle through a
specific type, and to give me a full test prep with a timer
```

**What was done:**

- Authored 11 new original LR questions (one each for the 11 official types
  not yet covered: sufficient_assumption, strengthen, weaken, inference,
  main_point, method_of_reasoning, principle, resolve_explain,
  evaluate_argument, point_at_issue, role_of_statement), matching the
  existing rigor bar (formal/conditional notation where applicable, named
  logical forms, every choice explicitly addressed) — added to
  `backend/app/mock_questions.py`, bringing the bank to 14 questions
  covering all 14 official LR types.
- **Independently verified all 11** via 11 parallel fresh subagents (Agent
  tool, `general-purpose` type) — each given only the stimulus/stem/
  choices/type (never the marked answer), asked to solve using the named
  method for that type. 11/11 matched my intended answer on the first pass;
  zero revisions needed.
- Validated schema (14 unique types, 5 choices each, valid answer letters),
  ran the full pytest suite (still 9/9 passing — no test changes needed),
  reseeded the DB (`scripts/generate_question.py`, mock mode), and
  curl-verified grading + `/api/stats/summary` aggregation work correctly
  across the new questions.
- **Bug fix (user-reported):** `GET /api/question/current` always did
  `ORDER BY id DESC LIMIT 1` (a leftover from when v0.1 only ever had one
  question) — with 14 questions now in the bank, this meant the app always
  served the single most-recently-seeded one, appearing to "repeat."
  Renamed `get_latest_question` → `get_random_question` in `db.py`
  (`ORDER BY RANDOM() LIMIT 1`), swapped it into the route in `main.py`.
  Kept the same route path (`/api/question/current`) to avoid unnecessary
  frontend churn. Verified live against the running dev server: 6
  consecutive calls returned 6 different question types. Tests still pass.
- Revised v0.1's Version Plan scope entry, Current State, and Key Decisions
  Log to reflect the new approach; the original live-API pipeline
  (`generation.py`, `prompts.py`, `GENERATION_MODE=live`) is untouched and
  remains available as an optional future path, just no longer required
  for v0.1.
- Per `CLAUDE.md`'s Finishing a Version checklist, did NOT commit, tag, or
  push yet — presenting the checklist next, for user confirmation.

**What broke / what to watch:**

- The `attempts` table has a handful of orphaned rows from before this
  session's reseed (old `question_id`s 1-3 got deleted by the seed
  script's wipe-and-reseed, but `attempts` has no cascade delete). This
  makes `get_overall_stats()`'s raw count drift slightly from
  `get_stats_by_type()`'s JOIN-filtered count (orphaned attempts silently
  excluded from the by-type breakdown). Pre-existing behavior, not
  introduced this session, and not something the user has asked to fix —
  noting it here so it isn't a surprise later, e.g. if v0.5 dedup work
  touches the `questions` table again.
- User has asked for three more things in the same message: (1) an
  explicit shuffle-through-all-types affordance — largely already
  satisfied by the random-serve fix above; (2) cycle through a specific
  type — this is v0.3's exact scope (filtered practice); (3) a full test
  with a timer — this is v0.6's scope, and v0.6's stated definition
  ("real blueprint: 2 LR + 1 RC") has a hard dependency on v0.2 (Reading
  Comprehension, not started). Flagged to the user in chat rather than
  building either inline as part of "finishing v0.1" — both are already
  their own scoped versions in the Version Plan, and pulling future-version
  work into the current one is exactly what the Versioning Strategy (and
  the checklist the user asked me to formalize) exists to prevent.

**Next session should:**

- Get user confirmation on this checklist, then commit + tag `v0.1` + push.
- Get the user's decision on ordering: v0.3 (filtered/cycle-by-type,
  small, unblocked) vs. v0.2 (RC, a prerequisite for a real-blueprint
  v0.6 timed test) vs. an explicitly-scoped LR-only interim timed-test
  version if the user doesn't want to wait for RC.

**Reconstruction prompt — v0.1 (revised scope):**

```
Rebuild this project (LSAT Prep) to v0.1's (revised) state: a Logical
Reasoning question bank, served and graded end-to-end, with NO live LLM
API dependency required.

TECH STACK:
- Backend: Python 3.11+, FastAPI, stdlib sqlite3 (no ORM), managed with uv.
  Dependencies: fastapi, uvicorn[standard], anthropic (used only by the
  optional live-generation path, not required for v0.1 itself),
  python-dotenv, pydantic; dev: pytest, httpx.
- Frontend: Next.js 16 (App Router, TypeScript), npm-managed.

PROJECT STRUCTURE:
backend/app/{main.py, db.py, models.py, config.py, generation.py,
  prompts.py, mock_questions.py, __init__.py}
backend/scripts/generate_question.py
backend/tests/{test_grading.py, test_stats.py}
frontend/app/{layout.tsx, page.tsx}
(v0.4's progress/page.tsx and stats plumbing, and v0.9's theme, are
separate versions layered on top — see their own reconstruction prompts.
This entry describes v0.1's layer only.)

FEATURES:

1. Question bank (the actual v0.1 deliverable): a SQLite `questions` table
   (id, section, question_type, content_area, stimulus, question_stem,
   choices [JSON array of 5 strings], correct_answer ["A"-"E"],
   explanation, verified [bool], created_at) populated with 14
   hand-authored original Logical Reasoning questions — one per official
   LR type (necessary_assumption, sufficient_assumption, strengthen,
   weaken, flaw, inference, main_point, method_of_reasoning,
   parallel_reasoning, principle, resolve_explain, evaluate_argument,
   point_at_issue, role_of_statement). Each question's explanation applies
   the official named method for its type explicitly (negation test for
   necessary assumption, named flaw taxonomy for flaw, conditional-logic
   notation for sufficient assumption/inference, abstracted structure
   comparison for parallel reasoning, etc.) and addresses every answer
   choice, not just the correct one.

2. Verification algorithm used to build the bank (the "foundation
   algorithm"): for each question, (a) author it following the named
   methodology for its type, (b) hand off to a FRESH context (a subagent
   with zero memory of which answer was marked correct) containing only
   the stimulus/stem/choices/type, (c) have it independently solve using
   the same named method, (d) only keep the question if its answer matches
   the intended one. No live API calls required - this runs once, during
   authoring, not at app runtime. (Historical note: an earlier version of
   this project attempted a live-Anthropic-API generate+verify pipeline at
   runtime instead - that code still exists at
   backend/app/generation.py/prompts.py, gated behind
   GENERATION_MODE=live in backend/app/config.py, but is NOT required and
   was never the mechanism that actually got v0.1 to a working state.)

3. Serving: `GET /api/question/current` returns a RANDOM question from the
   bank on every call (`ORDER BY RANDOM() LIMIT 1` in SQLite) - NOT the
   latest-inserted row (that was the original, buggy behavior when there
   was only ever one question; it silently became a "repeats the same
   question forever" bug once the bank grew past one row - watch for this
   if reimplementing naively). Response excludes correct_answer/explanation.

4. Grading: `POST /api/question/{id}/grade` takes {selected_answer},
   looks up the stored correct_answer, does a pure deterministic string
   comparison (no LLM call, no dependency on anything AI-related), returns
   {correct, correct_answer, explanation}. The explanation is always
   returned regardless of correctness, matching real LSAT prep convention.

5. Seeding: `backend/scripts/generate_question.py`, run as
   `uv run python scripts/generate_question.py` with `GENERATION_MODE=mock`
   (the default) - wipes the `questions` table and reinserts all 14 static
   questions from `mock_questions.py`. No API key needed for this path at
   all.

6. Frontend: a single page fetches the current (random) question, renders
   radio-button choices, submits an answer, and displays correct/incorrect
   plus the stored explanation.

KEY DECISIONS:
- The live-Anthropic-API path was explicitly de-scoped from v0.1's
  definition of "done," per user direction, after clarifying that
  "verified used questions" meant ORIGINAL hand-verified content, not real/
  copyrighted LSAT questions (real questions were flagged as a copyright
  risk and as directly conflicting with this project's own anti-
  memorization design goal - see CLAUDE.md Project Overview).
- Verification uses a fresh subagent re-solve (mirrors the exact method
  CLAUDE.md's Explanation Methodology section already specifies for live
  generation) rather than a live API call - same rigor, zero runtime cost/
  dependency.
- `GET /api/question/current`'s random-selection behavior was a direct fix
  to a real bug the user hit while testing (always serving the same
  question) - not a design choice made in isolation; if you rebuild this
  from scratch with a multi-question bank in mind from day one, make sure
  the "current question" endpoint is random/rotating from the start.

NOT YET IMPLEMENTED as of v0.1 (don't build ahead of scope):
- No Reading Comprehension (v0.2).
- No filtered/cycle-by-a-specific-type practice mode (v0.3) - though
  question_type is already stored per question, so this is mostly a
  filtering-endpoint + UI-control problem, not a data-model problem.
- No dedup/uniqueness check (v0.5) - not urgent yet since all 14 questions
  are original and hand-verified, but will matter once more get added.
- No full-length test assembly or timer (v0.6) - and note v0.6's stated
  definition requires RC (v0.2) for a real-blueprint test.
- No scaled scoring (v0.7), no deployment (v0.8).
- The live-API generate/verify pipeline exists in code but has never
  actually been run against the real Anthropic API - it's dead code from
  v0.1's original (abandoned) approach, kept intentionally as a possible
  future path, not deleted.
```

---

### [v0.4 + v0.9] Session 4 — 2026-08-09

**Prompt(s) used:**

```
why arent the versions in my readme.md checked off
[explained: nothing had cleared the "genuinely complete end-to-end" bar —
v0.1 blocked on API key, v0.4/v0.9 never visually confirmed in a browser]

Continue where we left off
```

**What was done:**

- Installed Playwright (`npx playwright install chromium`) — its own
  bundled Chromium, independent of the Homebrew `chromium` cask that was
  broken in Session 2 (cask present, `.app` binary missing). This is what
  unblocked real visual verification.
- Screenshotted `/` (unanswered state) and `/progress` via `npx playwright
  screenshot`, then wrote a small Playwright script (temporary, not part of
  the app) to actually select a radio choice, click Submit, and screenshot
  the graded result state — confirming the themed `.result-chip`
  (green "Correct! Correct answer: A") and the clean-card explanation
  render correctly together.
- Reviewed all three screenshots directly. Confirmed v0.4 and v0.9 both
  match their stated scope exactly (see reconstruction prompts below for
  the precise, now-verified state). Updated `prompt.md` (Current State,
  Version Plan status for v0.4/v0.9 → done) and `README.md` (checked off
  v0.4 and v0.9) accordingly.
- Per `CLAUDE.md`'s Finishing a Version checklist, did NOT commit, tag, or
  push yet — that requires presenting the user a checklist and waiting for
  explicit confirmation first (next step after this log entry).

**What broke / what to watch:**

- The temporary Playwright install went into `frontend/node_modules/`
  (gitignored, `--no-save` so `package.json`/`package-lock.json` untouched
  — confirmed via `git status` before and after). It's not a project
  dependency, just a one-off verification tool; harmless if left, fine to
  remove later.
- v0.1 is still blocked/incomplete — unrelated to and unaffected by this
  session's work.

**Next session should:**

- Present the finishing-a-version checklist for v0.4 + v0.9 to the user; on
  confirmation, commit, annotated-tag both (`v0.4`, `v0.9`), and push
  commit + tags.
- Separately, still need an `ANTHROPIC_API_KEY` to finish v0.1.

**Reconstruction prompt — v0.4:**

```
Rebuild this project (LSAT Prep) from an empty repo to exactly v0.4's state.

TECH STACK:
- Backend: Python 3.11+, FastAPI, stdlib sqlite3 (no ORM), managed with uv
  (pyproject.toml + uv.lock). Dependencies: fastapi, uvicorn[standard],
  anthropic, python-dotenv, pydantic; dev: pytest, httpx.
- Frontend: Next.js 16 (App Router, TypeScript), managed with npm. Uses
  next/font/google for the Geist font family (defaults from create-next-app
  at this version — no custom theme yet, that's v0.9).
- LLM: Anthropic API via the `anthropic` Python SDK, model "claude-sonnet-5".

PROJECT STRUCTURE:
backend/
  app/
    main.py, db.py, models.py, config.py, generation.py, prompts.py,
    mock_questions.py, __init__.py
  scripts/generate_question.py
  tests/__init__.py, test_grading.py, test_stats.py
  pyproject.toml, uv.lock, .env.example
  data/ (gitignored, sqlite file lives here)
frontend/
  app/layout.tsx, globals.css, page.tsx, progress/page.tsx, favicon.ico
  (+ standard Next.js scaffold files: next.config.ts, tsconfig.json,
  eslint.config.mjs, package.json)
.claude/skills/lsat-methodology/SKILL.md
.gitignore, .claudeignore, CLAUDE.md, prompt.md, README.md

FEATURES (full v0.1 base + v0.4 additions):

1. Question storage & generation (v0.1 base):
   - SQLite `questions` table: id, section, question_type, content_area
     (nullable), stimulus, question_stem, choices (JSON-encoded list of 5
     strings), correct_answer ("A"-"E"), explanation, verified (bool),
     created_at (ISO8601 UTC).
   - `GENERATION_MODE` env var (backend/app/config.py), default "mock".
     - mock mode: serves 3 hand-authored static LR questions from
       app/mock_questions.py (types: necessary_assumption, flaw,
       parallel_reasoning), each with a methodology-correct explanation
       (negation test / named flaw taxonomy / abstracted logical-structure
       comparison respectively). No API key needed.
     - live mode: app/generation.py's generate_and_verify() calls the
       Anthropic API to generate a question (system prompt in
       app/prompts.py embeds the full named-methodology reference for all
       14 official LR question types), then a SEPARATE fresh-context API
       call independently re-solves it; only stored if both agree; retries
       up to 3 times on mismatch, else raises GenerationError.
   - backend/scripts/generate_question.py: CLI that seeds the DB per
     GENERATION_MODE (mock: wipes and reseeds the 3 static questions; live:
     runs generate_and_verify() once and inserts the result).
   - FastAPI routes (backend/app/main.py):
     - GET /api/question/current — latest question, WITHOUT
       correct_answer/explanation.
     - POST /api/question/{id}/grade — body {selected_answer}. Looks up the
       stored correct_answer, compares (pure deterministic key-match, no
       LLM call), returns {correct, correct_answer, explanation}. ALSO
       inserts an attempts-table row as a documented side effect (see #2
       below) — this happens AFTER the comparison is computed and is never
       read back into the comparison.
     - POST /api/generate — wraps generate_and_verify(); returns 400 if
       GENERATION_MODE != "live".
   - CORS enabled for http://localhost:3000.

2. Attempts history + stats dashboard (v0.4 — this version's actual scope):
   - New SQLite `attempts` table: id, question_id (FK), selected_answer,
     correct (bool as int), explanation_viewed (bool as int — always 1 in
     this UI, since the grade response includes the explanation atomically;
     there's no separate "reveal" step to gate on yet), answered_at
     (ISO8601 UTC).
   - db.py: get_connection() executes the schema via
     conn.executescript(SCHEMA) (NOT conn.execute — breaks with
     "ProgrammingError: You can only execute one statement at a time" once
     SCHEMA has 2+ CREATE TABLE statements). insert_attempt(),
     get_overall_stats(), get_stats_by_type() (JOINs attempts to questions,
     groups by question_type), get_attempts_by_day() (groups by
     substr(answered_at, 1, 10)).
   - GET /api/stats/summary — returns StatsSummary: {overall: {total,
     correct, accuracy: float|null (null when total=0)}, by_type: [{
     question_type, total, correct, accuracy}], over_time: [{date, count}]}.
   - Frontend: app/layout.tsx adds a <nav> with "Practice" (/) and
     "Progress" (/progress) links (next/link). New app/progress/page.tsx
     (client component): fetches GET /api/stats/summary on mount, renders:
     a stat-tile with a big accuracy % + a meter bar (correct/total shown
     below); an "Accuracy by question type" section as a real HTML <table>
     where each row has the type name, a bar-track/bar-fill div sized by
     percentage, and the numeric value; an "Attempts over time" section,
     same bar-table pattern, one row per day.
   - globals.css: dashboard/theme values defined as CSS custom properties
     (--surface-1, --page-plane, --text-primary/secondary/muted, --gridline,
     --border, --series-1 [blue, single hue for magnitude per the dataviz
     skill's guidance], --series-1-track), both light and
     `@media (prefers-color-scheme: dark)` variants. Reusable classes:
     .stats-page, .stat-tile, .stat-tile-value, .meter-track/.meter-fill,
     .stats-section, .bar-table, .bar-track/.bar-fill. Deliberately
     token-based (not hardcoded hex in components) so a later visual theme
     could reskin by changing token values only.
   - Load the "dataviz" skill before writing any chart/dashboard UI code.

3. Testing: backend/tests/test_grading.py (5 tests: correct/incorrect
   grading, invalid answer letter, unknown question id, current-question
   never leaks the key) and test_stats.py (4 tests: empty-state summary,
   grading records an attempt with correct fields, failed grade requests —
   bad letter, unknown id — record nothing, multi-type aggregation is
   correct). All use a temp SQLite DB via pytest's tmp_path + monkeypatch,
   never touch the real backend/data/ DB, no live API calls in tests.

KEY DECISIONS:
- SQLite (stdlib, no ORM) chosen over Postgres/pgvector — sufficient for
  now, defers real DB infra until v0.5 (dedup) actually needs vector
  similarity search.
- Attempts logging is a pure side effect of grading — zero read dependency,
  so gamification/stats can never influence or be influenced by the
  deterministic grading result.
- Dashboard placed at v0.4 (right after v0.3's filtered practice, not after
  deploy) specifically because "accuracy by type" pairs with "go
  filter-practice your weak type" — motivating continued practice early
  rather than after every core feature ships.
- Only "Concept 1" (plain stats dashboard) was scoped — streaks, XP/levels,
  and mastery badges (Concepts 2 & 3) were explicitly proposed and then
  deferred to the Backlog, not built.

NOT YET IMPLEMENTED as of v0.4 (don't build ahead of scope):
- No visual theme — app is Next.js's default unstyled look at this version
  (theme is v0.9, a separate, later version).
- No Reading Comprehension (v0.2), no metadata-filtering UI (v0.3 — though
  the question_type/content_area columns already exist), no dedup (v0.5),
  no full-length test assembly (v0.6), no scaled scoring (v0.7), no
  deployment (v0.8).
- No streaks/XP/badges (deferred to Backlog, not this version).
- v0.1's live generate/verify pipeline exists in code but has never
  actually been run against the real Anthropic API — only mock mode has
  been exercised. This is inherited/known context, not part of v0.4's own
  scope to resolve.
```

**Reconstruction prompt — v0.9:**

```
Rebuild this project (LSAT Prep) from an empty repo to exactly v0.9's state.
This is everything in the v0.4 reconstruction prompt above, PLUS the
following visual theme layer (cosmetic/CSS + font changes only — no
grading/generation/data-model changes of any kind).

ADDITIONAL TECH: two Google Fonts added via next/font/google in
frontend/app/layout.tsx: Press Start 2P (weight 400, CSS var
--font-pixel-display) and Fredoka (CSS var --font-chrome-sans). Both
loaded alongside the existing Geist/Geist_Mono fonts.

VISUAL THEME ("Growtopia-inspired" — an ORIGINAL pixel-chunky look; no
sprites/logos/assets/branding from any actual game were sourced or copied,
and no "Growtopia" name/trademark appears anywhere in the app):

- Palette (frontend/app/globals.css, CSS custom properties, light + dark
  variants under `@media (prefers-color-scheme: dark)`): parchment page
  background (#fbf3dd light / #1e1712 dark), wood-brown panel/border colors
  (--wood-fill #8b5a2b, --wood-fill-hover #a9713a, --wood-shadow #4a2f17,
  --wood-highlight #c68b4a; dark-mode equivalents #5a3b1e/#6b4423/#241708/
  #8b5a2b), grass-green primary buttons (--btn-primary #388e3c light /
  #2e7d32 dark, with matching -highlight/-shadow bevel-edge steps), sky-blue
  secondary buttons (--btn-secondary #2a78d6/#3987e5 — same hex as the
  dashboard's --series-1, reused deliberately), fixed status colors for
  correct/incorrect (--status-good #0ca30c, --status-critical #d03b3b —
  same hex both light/dark, per the dataviz skill's palette convention that
  status colors are fixed, never themed). Every text-on-fill and
  data-series-vs-surface color pairing was run through the dataviz skill's
  `scripts/validate_palette.js` and clears >=3:1 contrast in both modes.
  The fixed status green/red pair fails the validator's CVD-separation
  check (expected and documented in the skill itself for that specific
  pair) — mitigated by NEVER conveying correct/incorrect by color alone:
  the UI always pairs it with a text label ("Correct!"/"Incorrect.").
- Reusable CSS classes (globals.css): `.wood-panel` (wood-grain texture via
  a repeating-linear-gradient of --wood-fill/--wood-highlight stripes at
  135deg, 3px --wood-shadow border, inset box-shadow bevel highlight/shadow
  edges). `.block-btn` (+ `.block-btn-primary` / `.block-btn-secondary`
  modifiers via CSS variable overrides) — chunky beveled buttons using the
  same inset-shadow bevel technique, with an :active state that inverts the
  highlight/shadow direction to read as "pressed in." `.result-chip` (+
  `.result-chip-correct` / `.result-chip-incorrect`) — small wood-bordered
  status chip, white text, background = --status-good or --status-critical.
  `.clean-card` — deliberately UNTHEMED: plain white/near-white background,
  plain system sans font (var(--font-geist-sans)), normal line-height —
  used for all long-form reading content.
- Fonts split by role (hard constraint from the user, not a stylistic
  choice): Press Start 2P (`var(--font-heading)`) reserved for headings
  (h1) and large stat-tile numbers ONLY — illegible at small sizes.
  Fredoka (`var(--font-chrome)`) used everywhere else in the themed chrome:
  nav links, button labels, dashboard section headings' sub-labels,
  bar-table row labels/values, result-chip text. Body default font-family
  on <body> is the chrome font; overridden back to the plain system font
  only inside `.clean-card`.
- Where the theme is applied vs. NOT applied (hard constraint from the
  user): nav (`.app-nav`, wood-panel background, each link styled as a
  small chunky wood block button), Submit/Reload buttons
  (`.block-btn-primary` / `.block-btn-secondary`), the /progress
  dashboard's stat-tile/stats-section panels (now `.wood-panel`-bordered
  with inset bevel, pixel-font headings/hero numbers, Fredoka-font
  labels/values, same blue --series-1 bars from v0.4 — only the
  surrounding chrome was reskinned, not the data-bar color itself), and the
  short correct/incorrect result chip on the practice page. NOT themed:
  frontend/app/page.tsx wraps the stimulus, question stem, answer choices,
  AND the post-grade explanation together inside a single `.clean-card` —
  all of that stays plain, high-contrast, system-font, specifically because
  it's long-form reading content (the explanation is prose just like the
  stimulus, so it gets the same treatment, not the themed-chrome treatment).

KEY DECISIONS SPECIFIC TO v0.9:
- Explanation text was deliberately classified as "reading content" (goes
  in .clean-card) rather than "chrome" (would get themed) — the user's
  constraint was "clean reading area, themed frame around it," and
  explanations are long-form prose exactly like the stimulus.
- The dashboard's data-bar color (blue, --series-1) was deliberately left
  as-is from v0.4 rather than re-hued to fit the wood/green palette more
  "thematically" — magnitude encoding should stay a single validated hue,
  and re-validating a new hue wasn't necessary when the existing one
  already passed against the new surfaces.
- No headless browser was available via the Homebrew `chromium` cask in
  this environment (binary missing) — visual verification required
  installing Playwright's own bundled Chromium (`npx playwright install
  chromium`) instead. If rebuilding in a similar sandboxed environment,
  expect the same and plan for it.

NOT YET IMPLEMENTED as of v0.9: same list as the v0.4 reconstruction prompt
above (RC, filtering UI, dedup, full-length assembly, scaled scoring,
deployment, streaks/XP/badges, and v0.1's live pipeline still unrun) — v0.9
added ONLY the visual theme layer on top of v0.4, nothing else.
```

---

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
