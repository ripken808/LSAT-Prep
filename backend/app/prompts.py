from app.mock_questions import MOCK_QUESTIONS

EXPLANATION_RIGOR_REQUIREMENTS = """
Explanation rigor requirements (apply regardless of question type):
1. Use consistent formal notation wherever the method calls for it - e.g.
   conditional logic as P -> Q, categorical claims as "All A are B" / "Some A
   are B", abstracted argument skeletons for parallel reasoning.
2. Name the specific logical form, flaw, or method explicitly (e.g. "affirming
   the consequent", "categorical syllogism", "causal reasoning flaw -
   reversed causation", "negation test"). Never just assert that a choice is
   "wrong" or "doesn't fit" without naming why.
3. Explicitly address EVERY answer choice, not just the correct one - e.g.
   negate all five choices for a necessary assumption question, give the
   abstracted structure of all five choices for parallel reasoning, explain
   why each of the four incorrect choices misdescribes the flaw for a flaw
   question.
"""

_REFERENCE_EXAMPLE = next(
    q for q in MOCK_QUESTIONS if q["question_type"] == "parallel_reasoning"
)


def _format_reference_example(question: dict) -> str:
    choices_block = "\n".join(
        f"{letter}. {text}"
        for letter, text in zip("ABCDE", question["choices"])
    )
    return (
        f"Question type: {question['question_type']}\n"
        f"Stimulus: {question['stimulus']}\n"
        f"Question stem: {question['question_stem']}\n"
        f"Choices:\n{choices_block}\n"
        f"Correct answer: {question['correct_answer']}\n"
        f"Explanation:\n{question['explanation']}"
    )


REFERENCE_EXAMPLE_BLOCK = f"""
Reference example (target quality bar - match this level of rigor for
whatever type you generate, not just parallel reasoning): consistent formal
notation, the logical form named explicitly for every choice, and explicit
structural comparison against every answer choice, not just the correct one.

{_format_reference_example(_REFERENCE_EXAMPLE)}
"""

METHODOLOGY_REFERENCE = """
Official LSAT Logical Reasoning question types and the named method that must
be used to justify the answer for each. When you write an explanation, you
must explicitly apply the named method below for whichever type the question
is — not a freeform paragraph that merely sounds plausible.

- necessary_assumption: Use the Negation Test explicitly. Negate the candidate
  answer; the correct answer's negation must make the argument's conclusion no
  longer follow (destroys the link between premises and conclusion). Negating
  an incorrect answer leaves the argument's logic intact.
- sufficient_assumption: State the premises and conclusion, identify the
  logical gap between them (often an undistributed middle term or an unproven
  link), express the relevant statements in conditional logic notation
  (e.g. P -> Q), and show how adding the correct answer as a premise lets the
  conclusion be validly chained/derived. Incorrect answers leave the gap open.
- strengthen: Identify the argument's unstated assumption (the gap between
  premises and conclusion), then show how the correct answer makes that
  assumption more plausible / adds support for it, without needing to prove
  the conclusion outright.
- weaken: Identify the argument's unstated assumption, then show how the
  correct answer attacks that assumption directly, giving a reason the
  conclusion may not follow even if the premises are true.
- flaw: Name the specific reasoning error using the recognized taxonomy (e.g.
  causal reasoning flaw [correlation-vs-causation, reversed causation, ignored
  alternative cause], equivocation [shifting meaning of a term],
  unrepresentative sample / hasty generalization, ad hominem, circular
  reasoning, false dichotomy, appeal to inappropriate authority,
  composition/division, confusing necessary and sufficient conditions, straw
  man) and show where in the argument it occurs.
- inference: (must-be-true) Show that the correct answer follows strictly by
  logical entailment from the stated premises alone, with no outside
  assumptions. Show why each incorrect answer either goes beyond what's
  stated or isn't fully supported.
- main_point: Identify the argument's premises, sub-conclusions, and ultimate
  conclusion using structural/indicator-word analysis, and show why the
  correct answer is the ultimate conclusion rather than a premise or
  sub-conclusion.
- method_of_reasoning: Describe the abstract argumentative technique the
  speaker uses (e.g. arguing by counterexample, analogy, applying a general
  principle to a specific case, appeal to authority) independent of topic.
- parallel_reasoning: Abstract the original argument into its logical
  skeleton (e.g. "All A are B; C is A; therefore C is B", or a conditional
  chain), then show the correct answer choice has the identical abstract
  structure and validity, and show at least one incorrect choice's structure
  diverges.
- principle: Either (a) state the general principle that, when applied,
  justifies the specific conclusion given [principle-justify], or (b)
  identify the specific case that correctly instantiates a stated general
  principle [principle-apply]. Show the match explicitly.
- resolve_explain: Identify the two facts that appear to conflict, then show
  how the correct answer supplies a new fact that lets both stated facts be
  true simultaneously without contradicting either.
- evaluate_argument: Identify the argument's central assumption/gap, then
  show that the correct answer is a question whose answer (yes vs. no) would
  reveal whether that gap is actually bridged.
- point_at_issue: Show that the correct answer is a claim about which the two
  speakers would give different answers (one would say yes/true, the other
  no/false) - not merely a topic both discuss.
- role_of_statement: Identify the function the specified statement plays in
  the argument's structure (premise, sub-conclusion, main conclusion,
  counter-consideration/objection being addressed, or background context),
  and justify why the other roles don't fit.
"""

GENERATION_SYSTEM_PROMPT = f"""You are an expert LSAT test writer. Generate one
ORIGINAL Logical Reasoning question in the style of the real LSAT. Do not copy
or lightly reword any real LSAT question - the stimulus, stem, and answer
choices must be novel content with a novel logical structure.

{METHODOLOGY_REFERENCE}
{EXPLANATION_RIGOR_REQUIREMENTS}
{REFERENCE_EXAMPLE_BLOCK}

Pick exactly one question type from the list above. Write a stimulus (2-6
sentences of argumentative text), a question stem appropriate to that type,
and exactly five answer choices (A-E) with exactly one correct answer. The
four incorrect choices must be plausible distractors, not obviously wrong.

Write the explanation by explicitly applying the named method for the type
you picked, per the reference above - show the actual reasoning work (e.g.
the negation test steps, the named flaw, the conditional-logic gap, the
abstracted structure), not just an assertion of which answer is correct. Match
the rigor and format of the reference example above.

Respond with ONLY a single JSON object (no markdown fences, no commentary),
with exactly these keys:
{{
  "question_type": "<one of: necessary_assumption, sufficient_assumption, strengthen, weaken, flaw, inference, main_point, method_of_reasoning, parallel_reasoning, principle, resolve_explain, evaluate_argument, point_at_issue, role_of_statement>",
  "stimulus": "<string>",
  "question_stem": "<string>",
  "choices": ["<A text>", "<B text>", "<C text>", "<D text>", "<E text>"],
  "correct_answer": "<one of A,B,C,D,E>",
  "explanation": "<string>"
}}
"""

VERIFY_SYSTEM_PROMPT = f"""You are an expert LSAT tutor doing independent
quality control on a Logical Reasoning question. You are given a stimulus,
question stem, question type, and five answer choices - but NOT the intended
correct answer. Solve it yourself from scratch by applying the official named
method for the given question type.

{METHODOLOGY_REFERENCE}
{EXPLANATION_RIGOR_REQUIREMENTS}

Respond with ONLY a single JSON object (no markdown fences, no commentary),
with exactly these keys:
{{
  "chosen_answer": "<one of A,B,C,D,E>",
  "explanation": "<string showing your independent application of the named method>"
}}
"""


def build_verify_user_message(question: dict) -> str:
    choices_block = "\n".join(
        f"{letter}. {text}"
        for letter, text in zip("ABCDE", question["choices"])
    )
    return (
        f"Question type: {question['question_type']}\n\n"
        f"Stimulus:\n{question['stimulus']}\n\n"
        f"Question stem: {question['question_stem']}\n\n"
        f"Choices:\n{choices_block}"
    )
