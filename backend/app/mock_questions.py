"""Hand-authored static Logical Reasoning questions used when
GENERATION_MODE=mock, so the app can be exercised end-to-end without calling
the (paid) Anthropic API. Each entry follows the same schema the live
generate_and_verify() pipeline produces, and each explanation applies the
official named LSAT methodology for its question_type per CLAUDE.md's
Explanation Methodology section.
"""

MOCK_QUESTIONS = [
    {
        "section": "logical_reasoning",
        "question_type": "necessary_assumption",
        "content_area": None,
        "stimulus": (
            "In the three months since additional security cameras were "
            "installed at Central Station, reported crimes at that station "
            "have decreased by 40 percent compared to the same period last "
            "year. Clearly, installing more security cameras throughout the "
            "subway system will significantly reduce crime system-wide."
        ),
        "question_stem": "The argument depends on assuming which one of the following?",
        "choices": [
            "No factor other than the additional cameras contributed to the decrease in reported crimes at Central Station during the three-month period.",
            "Security cameras are less expensive to install and maintain than hiring additional subway police officers.",
            "Central Station has more daily riders than any other station in the subway system.",
            "The subway system's overall ridership increased during the three-month period.",
            "Security cameras have been shown to reduce crime in a majority of the cities that have installed them.",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Necessary Assumption question, so the correct answer "
            "must pass the Negation Test: negating it should make the "
            "argument's conclusion collapse, while negating any incorrect "
            "answer should leave the argument's support intact.\n\n"
            "The argument reasons from a correlation (cameras installed, "
            "then reported crime fell 40%) to a causal claim (cameras caused "
            "the drop), and generalizes that cause system-wide. This is a "
            "classic causal-reasoning gap: it assumes no alternative "
            "explanation for the drop.\n\n"
            "(A) Negated: 'Some factor other than the cameras contributed to "
            "the decrease.' If true, the 40% drop may not be attributable to "
            "the cameras at all, so the claim that cameras will reduce crime "
            "system-wide loses its evidential support entirely - the "
            "argument falls apart. This is necessary.\n\n"
            "(B) Negated: cameras are NOT cheaper than officers. Cost is "
            "irrelevant to whether cameras reduce crime; the conclusion is "
            "untouched.\n"
            "(C) Negated: Central Station does NOT have the most riders. "
            "Ridership rank at one station has no bearing on the causal "
            "claim; conclusion untouched.\n"
            "(D) Negated: overall ridership did NOT increase. This doesn't "
            "affect whether cameras caused the reported-crime decrease; "
            "conclusion untouched.\n"
            "(E) Negated: cameras have NOT reduced crime in most cities that "
            "installed them. The argument's evidence is Central Station's own "
            "before/after data, not other cities' track records, so this "
            "would weaken confidence but doesn't destroy the specific causal "
            "inference being drawn here; it is not strictly necessary.\n\n"
            "Only (A)'s negation destroys the argument, so (A) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "flaw",
        "content_area": None,
        "stimulus": (
            "A study found that students who eat breakfast every day tend to "
            "have higher grade point averages than students who skip "
            "breakfast regularly. The study's authors concluded that eating "
            "breakfast every day causes students to earn higher grades. "
            "School administrators should therefore require all students to "
            "eat breakfast in order to raise grades school-wide."
        ),
        "question_stem": "The reasoning in the argument is most vulnerable to criticism on the grounds that it",
        "choices": [
            "presumes, without justification, that a correlation between two factors shows that one causes the other, when the higher grades might instead contribute to the breakfast habit, or some third factor might explain both",
            "fails to consider that not all students who eat breakfast every day have high grade point averages",
            "relies on a sample of students that is too small to be statistically meaningful",
            "draws a conclusion about all schools based on a study conducted at a single school",
            "presumes that grade point average is the only valid measure of academic success",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Flaw question, so the correct answer must name the "
            "specific reasoning error using the recognized taxonomy, not just "
            "assert that something is wrong.\n\n"
            "The argument's only evidence is a correlation between eating "
            "breakfast and higher GPA, yet its conclusion asserts a causal "
            "relationship (breakfast CAUSES higher grades) and then acts on "
            "that causal claim by recommending a policy. This is a textbook "
            "causal reasoning flaw: correlation-to-causation, specifically "
            "failing to rule out reverse causation (students who are already "
            "more disciplined or higher-achieving may be more likely to eat "
            "breakfast) and confounding variables (e.g. stable home "
            "environment could independently produce both habits). Choice "
            "(A) names exactly this.\n\n"
            "(B) is not a valid criticism: the argument is about a general "
            "tendency/average, not a universal claim, so exceptions don't "
            "undermine it.\n"
            "(C) isn't supported by the stimulus - no sample size is given, "
            "so this criticism can't be established from the text.\n"
            "(D) mischaracterizes the argument: the recommendation is "
            "'school-wide' (i.e., the same school), not a generalization to "
            "'all schools' - the stimulus never makes that broader claim.\n"
            "(E) is also unsupported: recommending a grade-focused policy "
            "doesn't require presuming GPA is the ONLY measure of academic "
            "success.\n\n"
            "Only (A) correctly identifies the argument's actual flaw."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "parallel_reasoning",
        "content_area": None,
        "stimulus": (
            "If a novel wins the National Book Award, it will be reviewed in "
            "every major newspaper. If a novel is reviewed in every major "
            "newspaper, its sales will increase substantially. Persuasion's "
            "Shadow won the National Book Award. So Persuasion's Shadow's "
            "sales will increase substantially."
        ),
        "question_stem": "Which one of the following arguments is most similar in its logical structure to the argument above?",
        "choices": [
            "If a bill passes committee, it will be scheduled for a floor vote. If a bill is scheduled for a floor vote, it will be debated by the full legislature. The clean water bill passed committee. So the clean water bill will be debated by the full legislature.",
            "If a restaurant earns a Michelin star, it will see a surge in reservations. Bistro Antoine saw a surge in reservations. So Bistro Antoine earned a Michelin star.",
            "If a car passes emissions testing, it may be legally registered. This car did not pass emissions testing. So this car may not be legally registered.",
            "If a student submits the application by the deadline, the student will be considered for the scholarship. Mia submitted her application by the deadline. So Mia will be considered for the scholarship.",
            "All finalists in the tournament receive a commemorative medal. Jordan is a finalist in the tournament. So Jordan will receive a commemorative medal.",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Parallel Reasoning question, so the correct answer "
            "must be found by abstracting the original argument into its "
            "logical skeleton and matching that exact form - not by matching "
            "topic or surface content.\n\n"
            "Original structure: Let P = 'wins the National Book Award', Q = "
            "'reviewed in every major newspaper', R = 'sales increase "
            "substantially'. The argument is: P -> Q, Q -> R, P is true, "
            "therefore R (a two-step conditional chain, valid by hypothetical "
            "syllogism plus modus ponens).\n\n"
            "(A): Let P = 'passes committee', Q = 'scheduled for a floor "
            "vote', R = 'debated by the full legislature'. Structure: P -> Q, "
            "Q -> R, P is true, therefore R. This is an exact structural "
            "match.\n\n"
            "(B): P -> Q, Q is true, therefore P - this affirms the "
            "consequent (a single conditional, invalid form) - different "
            "structure.\n"
            "(C): P -> Q, not-P, therefore not-Q - this denies the "
            "antecedent (a single conditional, invalid form) - different "
            "structure.\n"
            "(D): P -> Q, P is true, therefore Q - valid, but only a single "
            "conditional (simple modus ponens), not a two-step chain like the "
            "original - different structure.\n"
            "(E): 'All A are B; C is A; therefore C is B' - a categorical "
            "syllogism, not a conditional chain - different logical form "
            "entirely.\n\n"
            "Only (A) reproduces the original's exact two-link conditional-"
            "chain structure, so (A) is correct."
        ),
        "verified": True,
    },
]
