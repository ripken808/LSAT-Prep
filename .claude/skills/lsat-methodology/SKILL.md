---
name: lsat-methodology
description: Canonical LSAT Logical Reasoning methodology — the official named method for each question type, explanation-rigor requirements, and a target-quality reference example. Load this before writing or editing question-generation/explanation prompts (backend/app/prompts.py), reviewing generated question quality, or adding new LR question types, so methodology stays consistent instead of being re-derived ad hoc.
---

# LSAT Logical Reasoning Methodology

Per `CLAUDE.md`'s Explanation Methodology section, every explanation shown to
the user must apply the **official, named LSAT reasoning method** for that
question's type — not a freeform paragraph that merely sounds plausible. This
skill is the canonical reference so that stays consistent across sessions.

**Source of truth for code:** the methodology reference and rigor
requirements below are implemented in `backend/app/prompts.py`
(`METHODOLOGY_REFERENCE`, `EXPLANATION_RIGOR_REQUIREMENTS`) and fed into both
the generation and independent-verification system prompts. If you update the
methodology here, update `backend/app/prompts.py` to match, and vice versa.

## Named method per question type

- **necessary_assumption** — Negation Test: negate the candidate answer; the
  correct answer's negation must make the argument's conclusion no longer
  follow. Negating an incorrect answer leaves the argument's logic intact.
- **sufficient_assumption** — State premises/conclusion, identify the logical
  gap (often an undistributed middle term), express in conditional notation
  (`P -> Q`), and show how the correct answer closes the gap so the
  conclusion validly follows.
- **strengthen** — Identify the unstated assumption (the gap), show how the
  correct answer makes that assumption more plausible without needing to
  prove the conclusion outright.
- **weaken** — Identify the unstated assumption, show how the correct answer
  attacks it directly.
- **flaw** — Name the specific reasoning error using the recognized taxonomy
  (causal reasoning flaw [correlation-vs-causation, reversed causation,
  ignored alternative cause], equivocation, unrepresentative sample / hasty
  generalization, ad hominem, circular reasoning, false dichotomy,
  inappropriate appeal to authority, composition/division, confusing
  necessary and sufficient conditions, straw man) and show where it occurs.
- **inference** (must-be-true) — Show the correct answer follows strictly by
  logical entailment from the stated premises alone, no outside assumptions.
- **main_point** — Identify premises, sub-conclusions, and the ultimate
  conclusion via structural/indicator-word analysis.
- **method_of_reasoning** — Describe the abstract argumentative technique
  (arguing by counterexample, analogy, applying a general principle to a
  specific case, appeal to authority), independent of topic.
- **parallel_reasoning** — Abstract the original argument into its logical
  skeleton (conditional chain, categorical syllogism, etc.), then show the
  correct choice has the identical abstract structure/validity.
- **principle** — Either state the general principle that justifies the
  specific conclusion [principle-justify], or identify the specific case that
  instantiates a stated principle [principle-apply].
- **resolve_explain** — Identify the two facts that appear to conflict, show
  how the correct answer lets both be true simultaneously.
- **evaluate_argument** — Identify the central assumption/gap, show the
  correct answer is a question whose answer would reveal whether the gap is
  bridged.
- **point_at_issue** — Show the correct answer is a claim the two speakers
  would answer differently, not merely a shared topic.
- **role_of_statement** — Identify the statement's function (premise,
  sub-conclusion, main conclusion, counter-consideration, background), and
  justify why other roles don't fit.

## Named method per Reading Comprehension question type

RC questions are answered against a shared passage (`backend/app/rc_content.py`
→ `PASSAGES`, referenced by `passage_id` on `RC_QUESTIONS`), not a standalone
stimulus. Question types are prefixed `rc_` to keep them fully distinct from
LR types in the schema/stats (a passage can otherwise produce a "main_point"
question that isn't the same skill as an LR "main_point" question).

- **rc_main_point** — Identify the passage's primary purpose/thesis — what
  all paragraphs collectively build toward — not a sub-point developed in
  only one paragraph.
- **rc_specific_detail** — Correct answer must be explicitly stated in the
  passage (a direct textual lookup), not inferred. Incorrect answers either
  aren't stated or contradict the text.
- **rc_inference** — Must follow by logical entailment from stated passage
  content, no outside assumptions — same bar as LR inference, grounded in
  the passage.
- **rc_author_attitude** — Identify the author's attitude/tone toward a
  specific subject, based on evaluative word choice, not neutral factual
  content.
- **rc_passage_organization** — Describe the passage's abstract structural
  pattern (e.g. "presents a traditional view, then a critique, then an
  alternative"), not its content.
- **rc_analogous_situation** — Identify a new scenario sharing the same
  underlying structure/principle as something in the passage — parallels LR
  parallel_reasoning, applied to passage content.
- **rc_application** — Apply a principle/finding from the passage to a new
  context not explicitly discussed, extrapolating consistently with the text.
- **rc_strengthen_weaken** — Identify what would strengthen/weaken a specific
  claim or argument made within the passage (not the passage's overall main
  point).
- **rc_purpose_of_reference** — Identify why the author included a specific
  detail/example — its rhetorical function in the surrounding argument (e.g.
  "to illustrate," "to contrast," "to provide evidence for").
- **rc_meaning_in_context** — Determine what a word/phrase means as
  constrained by its surrounding sentences in the passage, not its
  dictionary definition in isolation.

## Explanation rigor requirements (apply to every type)

1. Use consistent formal notation wherever the method calls for it — `P -> Q`
   for conditionals, "All A are B" / "Some A are B" for categoricals,
   abstracted skeletons for parallel reasoning.
2. Name the specific logical form, flaw, or method explicitly (e.g.
   "affirming the consequent", "categorical syllogism", "causal reasoning
   flaw - reversed causation", "negation test"). Never just assert a choice
   is "wrong" without naming why.
3. Explicitly address **every** answer choice, not just the correct one —
   negate all five for necessary assumption, give the abstracted structure of
   all five for parallel reasoning, explain why each incorrect choice
   misdescribes the flaw for flaw questions, etc.

## Target-quality reference example (parallel_reasoning)

This is a hand-authored mock question (`backend/app/mock_questions.py`) that
hit the quality bar exactly — used verbatim as a few-shot example in the live
generation prompt (`backend/app/prompts.py` → `REFERENCE_EXAMPLE_BLOCK`).
When judging or writing any explanation (any type, not just parallel
reasoning), this is the standard to match: consistent formal notation, the
logical form named for every choice, and explicit structural comparison
against every answer choice.

**Stimulus:** If a novel wins the National Book Award, it will be reviewed in
every major newspaper. If a novel is reviewed in every major newspaper, its
sales will increase substantially. Persuasion's Shadow won the National Book
Award. So Persuasion's Shadow's sales will increase substantially.

**Question stem:** Which one of the following arguments is most similar in
its logical structure to the argument above?

**Choices:**
A. If a bill passes committee, it will be scheduled for a floor vote. If a
bill is scheduled for a floor vote, it will be debated by the full
legislature. The clean water bill passed committee. So the clean water bill
will be debated by the full legislature.
B. If a restaurant earns a Michelin star, it will see a surge in
reservations. Bistro Antoine saw a surge in reservations. So Bistro Antoine
earned a Michelin star.
C. If a car passes emissions testing, it may be legally registered. This car
did not pass emissions testing. So this car may not be legally registered.
D. If a student submits the application by the deadline, the student will be
considered for the scholarship. Mia submitted her application by the
deadline. So Mia will be considered for the scholarship.
E. All finalists in the tournament receive a commemorative medal. Jordan is a
finalist in the tournament. So Jordan will receive a commemorative medal.

**Correct answer:** A

**Explanation:**

This is a Parallel Reasoning question, so the correct answer must be found by
abstracting the original argument into its logical skeleton and matching
that exact form — not by matching topic or surface content.

Original structure: Let P = 'wins the National Book Award', Q = 'reviewed in
every major newspaper', R = 'sales increase substantially'. The argument is:
P -> Q, Q -> R, P is true, therefore R (a two-step conditional chain, valid
by hypothetical syllogism plus modus ponens).

(A): Let P = 'passes committee', Q = 'scheduled for a floor vote', R =
'debated by the full legislature'. Structure: P -> Q, Q -> R, P is true,
therefore R. This is an exact structural match.

(B): P -> Q, Q is true, therefore P — this affirms the consequent (a single
conditional, invalid form) — different structure.
(C): P -> Q, not-P, therefore not-Q — this denies the antecedent (a single
conditional, invalid form) — different structure.
(D): P -> Q, P is true, therefore Q — valid, but only a single conditional
(simple modus ponens), not a two-step chain like the original — different
structure.
(E): "All A are B; C is A; therefore C is B" — a categorical syllogism, not a
conditional chain — different logical form entirely.

Only (A) reproduces the original's exact two-link conditional-chain
structure, so (A) is correct.

## Where this is wired into the app

- `backend/app/prompts.py` — `METHODOLOGY_REFERENCE` and
  `EXPLANATION_RIGOR_REQUIREMENTS` are injected into both
  `GENERATION_SYSTEM_PROMPT` and `VERIFY_SYSTEM_PROMPT`.
  `REFERENCE_EXAMPLE_BLOCK` injects the example above into
  `GENERATION_SYSTEM_PROMPT` only (pulled live from
  `app.mock_questions.MOCK_QUESTIONS`, not duplicated by hand, so it can't
  drift from the actual mock data).
- `backend/app/mock_questions.py` — hand-authored static questions served in
  `GENERATION_MODE=mock`; the parallel_reasoning entry there is this skill's
  reference example.
- `backend/app/generation.py` — `generate_and_verify()` uses both prompts for
  the live generate → independent re-solve → retry-on-mismatch pipeline
  (only runs when `GENERATION_MODE=live`).
- `backend/app/rc_content.py` — hand-authored RC passages + questions (same
  verification method as LR: fresh subagent, no memory of the marked
  answer, independently re-solves before a question is kept).
