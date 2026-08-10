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
            "The decline in reported crimes at Central Station reflects, at least in part, a decline in the number of crimes actually committed there.",
            "The subway system's overall ridership did not change substantially during the three-month period.",
            "Security cameras have been shown to reduce crime in a majority of the cities that have installed them.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Necessary Assumption question, so the correct answer "
            "must pass the Negation Test: negating it should make the "
            "argument's conclusion collapse, while negating any incorrect "
            "answer should leave the argument's support intact. Note the bar "
            "is necessity, not sufficiency - an answer can be helpful, or "
            "even strongly supportive, and still be wrong here if the "
            "argument survives its negation.\n\n"
            "Watch the argument's terms shift: the evidence is about "
            "REPORTED crimes, while the conclusion is about reducing CRIME. "
            "The argument cannot get from one to the other unless the "
            "reported-crime figure tracks actual crime at least somewhat.\n\n"
            "(C) Negated: 'The decline in reported crimes reflects no decline "
            "whatever in crimes actually committed.' Then the 40% figure is "
            "an artifact of reporting behavior - perhaps cameras made riders "
            "less inclined to file reports - and the argument has zero "
            "evidence that any crime was prevented. The conclusion collapses. "
            "This is necessary, and it is correct.\n\n"
            "(A) Negated: 'Some factor other than the cameras contributed to "
            "the decrease.' The argument survives this: cameras can be a "
            "substantial cause of the drop even if better lighting or extra "
            "patrols also contributed, and a contributing cause is all the "
            "conclusion needs. (A) is the classic too-strong trap on "
            "Necessary Assumption questions - it would help the argument, "
            "but the argument does not depend on it.\n"
            "(B) Negated: cameras are NOT cheaper than officers. Cost is "
            "irrelevant to whether cameras reduce crime; conclusion "
            "untouched.\n"
            "(D) Negated: overall ridership DID change substantially. This "
            "raises an alternative explanation, weakening the argument, but "
            "does not destroy it - cameras could still be a genuine cause "
            "alongside a ridership change. Weakening is not the same as "
            "necessity.\n"
            "(E) Negated: cameras have NOT reduced crime in most cities that "
            "installed them. The argument's evidence is Central Station's own "
            "before/after data, not other cities' track records, so this "
            "lowers confidence without destroying the specific causal "
            "inference being drawn here; not strictly necessary.\n\n"
            "Only (C)'s negation destroys the argument, so (C) is correct."
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
            'presumes, without justification, that a correlation between two factors establishes that the first of them causes the second',
            'fails to consider that not every student who eats breakfast daily achieves a high grade point average, nor every skipper a low one',
            'relies on a study whose sample of students is far too small for its results to be statistically meaningful',
            'draws a conclusion about schools generally from a study conducted at only a single school in one district',
            "presumes, without any support, that grade point average is the only valid measure of a student's academic success",
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
            'If a bill passes committee, it will be scheduled for a floor vote. If a bill is scheduled for a floor vote, it will be debated by the full legislature. The clean water bill passed committee. So it will be debated by the full legislature.',
            "If a restaurant earns a Michelin star, it will see a surge in reservations. Bistro Antoine saw a surge in reservations. So Bistro Antoine earned a Michelin star.",
            'If a car passes emissions testing, it may be legally registered in the state. This particular car did not pass emissions testing. So this car may not be legally registered anywhere in the state.',
            "If a student submits the application by the deadline, the student will be considered for the scholarship. Mia submitted her application by the deadline. So Mia will be considered for the scholarship.",
            'All finalists in the regional tournament receive a commemorative medal at the closing ceremony. Jordan is a finalist in the regional tournament. So Jordan will receive a commemorative medal.',
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
    {
        "section": "logical_reasoning",
        "question_type": "sufficient_assumption",
        "content_area": None,
        "stimulus": (
            "All research scientists at Meridian Labs have a PhD in a "
            "natural science. Dr. Osei does not have a PhD in a natural "
            "science. Therefore, Dr. Osei is not eligible for the "
            "department director position at Meridian Labs."
        ),
        "question_stem": "The conclusion follows logically if which one of the following is assumed?",
        "choices": [
            "Everyone with a natural-science PhD is a research scientist at Meridian Labs.",
            "Dr. Osei has never applied for the department director position.",
            "Only current research scientists at Meridian Labs are eligible for the department director position.",
            "Most research scientists at Meridian Labs do not wish to become department director.",
            "Meridian Labs prefers to promote from within rather than hire external candidates for director.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Sufficient Assumption question, so the correct answer "
            "must be shown, via conditional logic, to close the gap between "
            "premises and conclusion so the conclusion follows validly.\n\n"
            "Let R = 'is a research scientist at Meridian Labs', S = 'has a "
            "natural-science PhD', E = 'is eligible for department director'. "
            "Premises: R -> S (all research scientists have the PhD); "
            "not-S(Osei). By modus tollens, not-R(Osei) - Osei is not a "
            "research scientist. The conclusion is not-E(Osei). Nothing "
            "given links research-scientist status to director eligibility - "
            "that is the gap.\n\n"
            "(C) supplies E -> R (only research scientists are eligible), "
            "equivalently not-R -> not-E by contraposition. Combined with "
            "not-R(Osei) already derived, this validly yields not-E(Osei). "
            "The gap is closed.\n\n"
            "(A) gives S -> R, the converse of the first premise - it does "
            "not connect research-scientist status to eligibility at all.\n"
            "(B) is about whether Osei applied, not about eligibility - "
            "irrelevant to the logical gap.\n"
            "(D) is about research scientists' desires, not eligibility "
            "criteria - doesn't bear on whether Osei specifically is "
            "eligible.\n"
            "(E) is about the lab's general hiring preference, not a rule "
            "that would make Osei categorically ineligible - doesn't "
            "guarantee the conclusion.\n\n"
            "Only (C) makes the conclusion follow with logical certainty, so "
            "(C) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "strengthen",
        "content_area": None,
        "stimulus": (
            "Ridgeline Elementary School introduced a 15-minute recess "
            "before lunch instead of after lunch last year. Since the "
            "change, the school's cafeteria reports a 30 percent decrease "
            "in uneaten food being thrown away. School administrators "
            "conclude that having recess before lunch causes students to "
            "eat more of their meals."
        ),
        "question_stem": "Which one of the following, if true, most strengthens the administrators' argument?",
        "choices": [
            "Ridgeline Elementary's cafeteria has employed the same number of kitchen staff over each of the past two school years.",
            "Several other elementary schools in the district have also reported decreases in cafeteria food waste this year.",
            "Ridgeline Elementary's cafeteria staff received training on portion control shortly before the schedule change.",
            'Students who have recess before lunch report feeling less rushed and hungrier when they sit down to eat than students who do not.',
            'Students at Ridgeline Elementary hold mixed opinions about whether they would prefer to have recess before lunch or after it.',
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Strengthen question. The argument infers a causal "
            "claim (recess-before-lunch causes more eating) from a "
            "correlation (schedule change, then less food waste). The gap is "
            "the unstated assumption that the schedule change itself, and "
            "not some other factor, produced the effect - a Strengthen "
            "answer should make that causal link more plausible, typically "
            "by supplying a mechanism.\n\n"
            "(D) directly supplies the mechanism: students are less rushed "
            "and hungrier before eating, which plausibly explains why they "
            "eat more of their food. This makes the causal claim more "
            "credible without proving it outright, which is exactly the "
            "Strengthen bar (lower than Sufficient Assumption).\n\n"
            "(A) is irrelevant: how many kitchen staff the cafeteria employs "
            "bears on how food is prepared and served, not on whether the "
            "recess schedule changed how much of it students ate.\n"
            "(B) actually cuts against the argument by suggesting a "
            "district-wide trend unrelated to Ridgeline's specific schedule "
            "change could explain the drop.\n"
            "(C) introduces a competing explanation (staff portion-control "
            "training) that could account for the waste decrease "
            "independent of the schedule change - if anything this weakens.\n"
            "(E) is irrelevant: student preference doesn't bear on whether "
            "the schedule change causally reduced waste.\n\n"
            "Only (D) strengthens the argument, so (D) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "weaken",
        "content_area": None,
        "stimulus": (
            "A recent survey found that employees at Trenton Manufacturing "
            "who participate in the company's optional wellness program "
            "use, on average, three fewer sick days per year than employees "
            "who do not participate. The company's HR director concludes "
            "that the wellness program causes employees to take fewer sick "
            "days, and plans to make participation mandatory for all "
            "employees to reduce absenteeism company-wide."
        ),
        "question_stem": "Which one of the following, if true, most seriously weakens the HR director's argument?",
        "choices": [
            'The wellness program includes gym membership discounts, healthy-eating seminars, and on-site fitness classes.',
            'Employees who opt into the optional program already prioritize their health and take fewer sick days regardless of it.',
            'Trenton Manufacturing has offered the optional wellness program to its employees for each of the past five years.',
            'Some employees who do not participate in the wellness program also take very few sick days in a given year.',
            'The wellness program costs the company a modest amount per participating employee in each year of its operation.',
        ],
        "correct_answer": "B",
        "explanation": (
            "This is a Weaken question. The HR director infers causation "
            "(the program causes fewer sick days) from a correlation "
            "(participants average fewer sick days), and further assumes "
            "this causal effect will transfer to employees who did not "
            "voluntarily choose to participate. The unstated assumption is "
            "that participants and non-participants don't differ in "
            "relevant ways apart from the program itself.\n\n"
            "(B) attacks that assumption directly: it's a self-selection "
            "explanation - health-conscious employees who already take "
            "fewer sick days are the ones who opt into the program, so the "
            "correlation may reflect a pre-existing difference rather than "
            "an effect of the program. This also undercuts the plan to make "
            "participation mandatory, since the observed benefit may not "
            "apply to people who wouldn't have joined voluntarily.\n\n"
            "(A) describes the program's contents but doesn't bear on "
            "whether it causes fewer sick days.\n"
            "(C) is irrelevant to the causal claim.\n"
            "(D) doesn't weaken an average-based claim - a few "
            "non-participants with low sick-day use is consistent with "
            "participants still averaging fewer.\n"
            "(E) is about cost, not about whether the causal claim is true.\n\n"
            "Only (B) undermines the argument's causal inference, so (B) is "
            "correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "inference",
        "content_area": None,
        "stimulus": (
            "Every member of the Lakeside Rowing Club who competed in the "
            "spring regatta also attended at least four winter training "
            "sessions. No one who attended fewer than four winter training "
            "sessions was permitted to use the club's racing shells. Priya, "
            "a member of the Lakeside Rowing Club, was permitted to use the "
            "club's racing shells this winter."
        ),
        "question_stem": "If the statements above are true, which one of the following must also be true?",
        "choices": [
            "Priya competed in the spring regatta.",
            "Priya attended more winter training sessions than any other member who competed in the spring regatta.",
            "Every member of the Lakeside Rowing Club was permitted to use the club's racing shells this winter.",
            "No member who competed in the spring regatta was denied permission to use the club's racing shells.",
            "Priya attended at least four winter training sessions this year.",
        ],
        "correct_answer": "E",
        "explanation": (
            "This is an Inference (must-be-true) question, so the correct "
            "answer must follow strictly by logical entailment from the "
            "premises alone, with no outside assumptions.\n\n"
            "The second premise, 'no one who attended fewer than four "
            "sessions was permitted to use the racing shells,' is "
            "equivalent to: permitted -> attended at least four sessions. "
            "Priya was permitted, so by this conditional, Priya attended at "
            "least four winter training sessions. This is (E), and it "
            "follows with certainty.\n\n"
            "(A) is not entailed: the first premise only says competing -> "
            "attended at least four sessions, not the converse. Concluding "
            "Priya competed from her session attendance would be affirming "
            "the consequent - a common trap, not a valid inference.\n"
            "(B) is not entailed: no comparative information about session "
            "counts is given.\n"
            "(C) is not entailed: only Priya's permission status is stated; "
            "nothing is said about every member.\n"
            "(D) is not entailed: the premises link permission to session "
            "count, not to regatta participation directly, and nothing "
            "states that attending four sessions guarantees permission (only "
            "the reverse) - so this can't be derived.\n\n"
            "Only (E) is strictly entailed, so (E) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "main_point",
        "content_area": None,
        "stimulus": (
            "Critics of urban food co-ops argue that their membership-fee "
            "model excludes low-income residents, undermining their stated "
            "mission of expanding access to affordable, healthy food. But "
            "most co-ops offer sliding-scale fees, fee waivers for "
            "low-income members, and volunteer-hour alternatives to cash "
            "payment. Moreover, studies show that co-op membership in "
            "low-income neighborhoods has grown steadily over the past "
            "decade. While co-ops are not a complete solution to food "
            "access problems, the criticism that their fee structure "
            "inherently excludes low-income residents is not well-"
            "supported by the evidence."
        ),
        "question_stem": "Which one of the following most accurately expresses the main point of the argument?",
        "choices": [
            "Most urban food co-ops offer sliding-scale fees, fee waivers, and volunteer-hour alternatives to cash payment.",
            "Urban food co-ops are a complete solution to food access problems in low-income neighborhoods.",
            "Co-op membership in low-income neighborhoods has grown steadily over the past decade.",
            "The criticism that co-ops' fee structure inherently excludes low-income residents is not well-supported by the evidence.",
            "Critics of urban food co-ops are mainly concerned with the co-ops' membership-fee model.",
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Main Point question, so the correct answer must be "
            "the argument's ultimate conclusion, identified via structural "
            "analysis - not a premise or sub-point offered in its support.\n\n"
            "The passage opens by presenting the critics' claim (background), "
            "then offers two premises (sliding-scale/waiver options; "
            "membership growth in low-income areas), and closes with 'the "
            "criticism ... is not well-supported by the evidence' - signaled "
            "as the takeaway by the concluding position after 'while co-ops "
            "are not a complete solution.' That closing claim, (D), is what "
            "the premises are marshalled to support.\n\n"
            "(A) and (C) are each one of the two premises offered in support "
            "of (D), not the conclusion itself.\n"
            "(B) misstates the argument, which explicitly denies co-ops are "
            "a complete solution.\n"
            "(E) describes the critics' concern, not the author's own "
            "concluding claim.\n\n"
            "Only (D) is the ultimate conclusion, so (D) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "method_of_reasoning",
        "content_area": None,
        "stimulus": (
            "Economist: Some argue that raising the minimum wage always "
            "leads to higher unemployment among low-wage workers, since "
            "employers facing higher labor costs will hire fewer workers. "
            "But consider the restaurant industry in Belmont County after "
            "its minimum wage increase last year: total restaurant "
            "employment there actually rose by four percent. If raising "
            "the minimum wage always caused higher unemployment, we would "
            "not expect to see employment increase in an industry "
            "immediately after such an increase. Therefore, the claim that "
            "raising the minimum wage always leads to higher unemployment "
            "is false."
        ),
        "question_stem": "The economist's argument proceeds by which one of the following methods of reasoning?",
        "choices": [
            "Establishing a causal relationship by ruling out all alternative explanations for an observed correlation.",
            "Appealing to the authority of economic experts to support a policy conclusion.",
            "Drawing an analogy between two similar but distinct economic situations.",
            "Demonstrating that an opposing argument is internally self-contradictory.",
            "Undermining a universal claim by citing a specific case that is inconsistent with what the claim predicts.",
        ],
        "correct_answer": "E",
        "explanation": (
            "This is a Method of Reasoning question, so the correct answer "
            "must describe the argument's abstract technique, independent of "
            "its topic.\n\n"
            "The economist targets a universal claim ('always leads to "
            "higher unemployment'), then points to one specific case "
            "(Belmont County restaurant employment rose after the increase) "
            "that is inconsistent with what the universal claim predicts, "
            "and concludes the universal claim must be false. This is "
            "refutation by counterexample - naming a case the universal rule "
            "cannot account for. (E) names exactly this method.\n\n"
            "(A) is wrong: the economist isn't establishing a causal "
            "relationship or ruling out alternative explanations for "
            "anything.\n"
            "(B) is wrong: no expert authority is invoked.\n"
            "(C) is wrong: no analogy between distinct situations is drawn - "
            "Belmont County is used as a direct counterexample, not an "
            "analogous case.\n"
            "(D) is wrong: the economist doesn't show the opposing view is "
            "self-contradictory, only that it conflicts with an observed "
            "fact.\n\n"
            "Only (E) correctly names the method used, so (E) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "principle",
        "content_area": None,
        "stimulus": (
            "The city council fined Greenfield Manufacturing for violating "
            "a noise ordinance, even though the factory's noise levels were "
            "within legal limits during the day. The violation occurred "
            "because the factory ran late-night shifts that produced noise "
            "levels exceeding the ordinance's nighttime limits, disturbing "
            "nearby residents. The council's fine was appropriate."
        ),
        "question_stem": "Which one of the following principles, if valid, most helps to justify the city council's decision to fine Greenfield Manufacturing?",
        "choices": [
            'A business should be fined for an ordinance violation only if the violation was intentional rather than inadvertent.',
            'Noise ordinances should impose the same decibel limits on daytime and on nighttime industrial operations alike.',
            "A business should be fined if its operations exceed an ordinance's limits during any period the ordinance covers.",
            'A business that complies with an ordinance during the majority of its operating hours should not be fined at all.',
            'Fines for noise ordinance violations should be proportional to the number of nearby residents actually affected.',
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Principle (principle-justify) question: the correct "
            "answer must be a general rule that, applied to these specific "
            "facts, justifies the specific judgment reached (fining "
            "Greenfield despite daytime compliance).\n\n"
            "(C) states that exceeding an ordinance's limits during any "
            "covered period is finable even with compliance during other "
            "periods. Applied here: Greenfield complied during the day but "
            "violated the nighttime limits - under (C), that is still "
            "properly finable. This directly justifies the council's "
            "decision.\n\n"
            "(A) would undermine the fine, since the stimulus gives no "
            "evidence the nighttime violation was intentional - adopting (A) "
            "would make it harder, not easier, to justify the fine.\n"
            "(B) is about equal application across day/night, not about how "
            "to treat a business that complies in one period and violates in "
            "another - it doesn't address the specific judgment being made.\n"
            "(D) directly argues AGAINST fining Greenfield, since Greenfield "
            "complied during the day (the majority of typical operating "
            "hours) - this contradicts the council's decision rather than "
            "justifying it.\n"
            "(E) introduces a proportionality standard the stimulus never "
            "addresses (no information about number of residents affected).\n\n"
            "Only (C) justifies the specific decision, so (C) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "resolve_explain",
        "content_area": None,
        "stimulus": (
            "Marathon runners typically slow their pace significantly in "
            "the final six miles of a 26.2-mile race, a phenomenon often "
            "attributed to glycogen depletion (\"hitting the wall\"). Yet in "
            "last month's Cedar City Marathon, the winning runner actually "
            "ran her final six miles faster than her first six miles, "
            "despite having consumed no more calories during the race than "
            "the average finisher."
        ),
        "question_stem": "Which one of the following, if true, most helps to resolve the apparent discrepancy described above?",
        "choices": [
            'Glycogen depletion is the single most common cause of slowing during the final miles of a marathon.',
            'The winning runner has won several other marathons over the past three racing seasons.',
            'The Cedar City Marathon course is relatively flat compared with most other marathon courses.',
            'The winning runner deliberately ran her first six miles well below her natural race pace.',
            'Average finishers in the Cedar City Marathon consumed sports drinks at aid stations during the race.',
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Resolve/Explain question. The apparent conflict: "
            "runners typically slow in the final miles due to glycogen "
            "depletion, yet this runner sped up despite ordinary caloric "
            "intake. The correct answer must supply a new fact that lets "
            "both the general phenomenon and this runner's result be true "
            "at once.\n\n"
            "(D) explains it via pacing strategy: by deliberately running "
            "the early miles conservatively, she preserved more energy for "
            "the finish, producing a negative split without contradicting "
            "the general 'hitting the wall' phenomenon for runners who go "
            "out at their natural (faster) early pace.\n\n"
            "(A) restates the general premise; it doesn't explain why this "
            "runner was an exception.\n"
            "(B) is irrelevant to this race's specific pacing pattern.\n"
            "(C) would affect all runners in the race equally and doesn't "
            "explain why THIS runner, specifically, sped up.\n"
            "(E) doesn't address the winning runner's own caloric intake or "
            "pacing pattern.\n\n"
            "Only (D) resolves the discrepancy, so (D) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "evaluate_argument",
        "content_area": None,
        "stimulus": (
            "A city planner argues: \"Installing roundabouts at the three "
            "most accident-prone intersections in Millbrook will reduce "
            "traffic collisions there, because roundabouts have been shown "
            "to reduce collisions at intersections in several other "
            "cities.\""
        ),
        "question_stem": "The answer to which one of the following questions would be most useful in evaluating the city planner's argument?",
        "choices": [
            'How much will it cost the city of Millbrook to install roundabouts at the three intersections?',
            'Have other cities that installed roundabouts also made additional traffic safety improvements at the same time?',
            "How long has Millbrook's city council been discussing possible traffic safety improvements downtown?",
            'Do most licensed drivers in Millbrook support the installation of roundabouts at those intersections?',
            "Are Millbrook's three intersections similar in traffic volume and geometry to those in the other cities?",
        ],
        "correct_answer": "E",
        "explanation": (
            "This is an Evaluate the Argument question, so the correct "
            "answer must be a question whose answer would reveal whether the "
            "argument's central assumption actually holds.\n\n"
            "The argument relies on an analogy: because roundabouts reduced "
            "collisions at 'intersections in several other "
            "cities,' they will do the same in Millbrook. The central "
            "assumption is that Millbrook's intersections are, in fact, "
            "comparable to those other intersections. (E) asks exactly this "
            "- a 'no' answer would seriously undermine the argument, a "
            "'yes' would support it.\n\n"
            "(A) bears on affordability, not on whether the roundabouts "
            "would actually reduce collisions. Cost tells you whether the "
            "project is worth doing, never whether the causal claim is "
            "true - a different question from the one the argument makes.\n"
            "(C) is irrelevant to whether roundabouts would work.\n"
            "(D) driver opinion doesn't bear on whether collisions would "
            "actually decrease.\n"
            "(B) touches on a possible confound in the other cities' data, "
            "but is less directly tied to the argument's specific analogical "
            "assumption than (E), which asks about the Millbrook "
            "intersections themselves.\n\n"
            "Only (E) most directly tests the argument's key assumption, so "
            "(E) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "point_at_issue",
        "content_area": None,
        "stimulus": (
            "Marcus: The city should replace all street lighting with LED "
            "fixtures. LEDs use significantly less electricity than the "
            "sodium-vapor lights currently installed, so the switch would "
            "reduce the city's energy costs substantially.\n"
            "Diane: I agree LEDs use less electricity per fixture, but the "
            "up-front cost of replacing every sodium-vapor fixture citywide "
            "would be so high that it would take over twenty years for the "
            "energy savings to offset the initial investment. Given the "
            "city's tight budget, that's too long a payback period to "
            "justify the switch right now."
        ),
        "question_stem": "Marcus and Diane disagree over whether",
        "choices": [
            "LED fixtures use less electricity than sodium-vapor fixtures",
            "the city has a tight budget",
            "the city should replace its street lighting with LED fixtures at this time",
            "LED fixtures have a higher up-front cost than sodium-vapor fixtures",
            "energy costs are the most important factor in choosing street lighting",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Point at Issue question, so the correct answer must "
            "be a claim the two speakers would actually answer differently - "
            "not merely a topic they both discuss.\n\n"
            "Marcus advocates switching to LEDs without qualification; Diane "
            "explicitly says the payback period is 'too long ... to justify "
            "the switch right now.' They give opposite answers to whether "
            "the city should make the switch now - (C).\n\n"
            "(A) is explicitly conceded by Diane ('I agree LEDs use less "
            "electricity') - not a point of disagreement.\n"
            "(B) is asserted by Diane and never disputed by Marcus - not "
            "shown to be contested.\n"
            "(D) is implied by both (Diane states it; Marcus's argument for "
            "long-term savings presupposes an up-front cost) and never "
            "disputed.\n"
            "(E) neither speaker makes this comparative priority claim.\n\n"
            "Only (C) is a genuine, textually-supported disagreement, so (C) "
            "is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "role_of_statement",
        "content_area": None,
        "stimulus": (
            "Nutritionists have long recommended that adults consume at "
            "least five servings of fruits and vegetables daily. Some "
            "critics argue that this guideline is unrealistic for "
            "low-income families, given the relatively high cost of fresh "
            "produce compared to processed foods. However, frozen and "
            "canned fruits and vegetables, which are typically much less "
            "expensive than fresh produce, retain most of the same "
            "nutritional value. Therefore, the five-a-day guideline remains "
            "achievable for low-income families, provided they are aware "
            "that frozen and canned options count toward it."
        ),
        "question_stem": "The claim that frozen and canned fruits and vegetables are typically much less expensive than fresh produce plays which one of the following roles in the argument?",
        "choices": [
            'It is the main conclusion that the argument as a whole is designed to establish.',
            "It is a claim that the argument's author introduces and then explicitly rejects as false.",
            "It is an objection to the argument's main conclusion that the author fails to adequately address.",
            'It is a premise supporting the conclusion that the five-a-day guideline remains achievable for low-income families.',
            "It is background information that is ultimately irrelevant to the argument's stated conclusion.",
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Role of a Statement question, so the correct answer "
            "must identify the specified claim's function in the argument's "
            "structure.\n\n"
            "The claim that frozen/canned produce is much less expensive is "
            "used to counter the critics' cost objection and to support the "
            "argument's final conclusion that the guideline 'remains "
            "achievable for low-income families.' It is evidence offered in "
            "support of that conclusion - (D).\n\n"
            "(A) is wrong: the main conclusion is the achievability claim at "
            "the end, not this cost claim.\n"
            "(B) is wrong: the author relies on and asserts this claim, "
            "doesn't reject it.\n"
            "(C) is wrong: it functions as supporting evidence for the "
            "author's rebuttal, not as an unaddressed objection.\n"
            "(E) is wrong: the claim is directly relevant - it's the key "
            "evidence the rebuttal depends on, not mere background.\n\n"
            "Only (D) correctly identifies its role, so (D) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "necessary_assumption",
        "content_area": None,
        "stimulus": (
            "Museum director: Our attendance rose 25 percent in the year "
            "after we began offering free admission on Sundays. Free Sunday "
            "admission has therefore been good for the museum's finances, "
            "since higher attendance means more revenue from the gift shop "
            "and cafe."
        ),
        "question_stem": (
            "The director's argument depends on assuming which one of the "
            "following?"
        ),
        "choices": [
            "The museum's gift shop and cafe were open to visitors on Sundays.",
            "No visitor who would otherwise have paid full admission on another day chose instead to visit on a free Sunday.",
            "The museum's Sunday attendance is now higher than its attendance on any other day of the week.",
            "The museum's operating costs did not increase during the year in question.",
            "Most museums that offer a free admission day experience a comparable increase in attendance.",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Necessary Assumption question, so apply the Negation "
            "Test: the correct answer is the one whose negation destroys the "
            "argument. An answer that merely helps the argument is not "
            "enough.\n\n"
            "The conclusion is financial ('good for the museum's finances'), "
            "but the whole case runs through one channel: free Sundays draw "
            "more people, and those people spend at the gift shop and cafe. "
            "Every link in that chain is something the argument needs.\n\n"
            "(A) Negated: 'The gift shop and cafe were NOT open on Sundays.' "
            "Then the extra Sunday visitors can spend nothing at either one, "
            "the only revenue mechanism the director offers disappears, and a "
            "policy that gives away admission while generating no offsetting "
            "income is not good for the museum's finances. The argument "
            "collapses, so (A) is necessary and correct. Note that it is "
            "worded affirmatively rather than as a hedge - a necessary "
            "assumption does not have to contain 'not entirely' or 'at least "
            "in part' to pass the negation test.\n\n"
            "(B) Negated: 'Some visitor who would have paid on another day "
            "came on a free Sunday instead.' The argument survives easily - "
            "a handful of shifted visits does not undo a 25 percent "
            "attendance rise. This is the too-strong trap: helpful if true, "
            "but not something the argument depends on.\n"
            "(C) Negated: Sunday is not the busiest day. Irrelevant - the "
            "argument compares the museum to its own past, not its days to "
            "each other.\n"
            "(D) Negated: operating costs did increase. A cost increase from "
            "some unrelated source does not show that the free-Sunday policy "
            "specifically was bad for finances, which is the only claim at "
            "issue. Tempting, but not necessary.\n"
            "(E) Negated: other museums do not see comparable increases. "
            "This museum's own attendance data is the evidence; other "
            "museums' results are beside the point.\n\n"
            "Only (A)'s negation destroys the argument, so (A) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "necessary_assumption",
        "content_area": None,
        "stimulus": (
            "Editorial: The city's bike-share program has succeeded in "
            "reducing traffic congestion. Since the program launched two "
            "years ago, average rush-hour travel times on the city's main "
            "arteries have fallen by eight percent."
        ),
        "question_stem": (
            "The editorial's argument requires the assumption that"
        ),
        "choices": [
            "the bike-share program is the only measure the city has taken to address traffic congestion",
            "most bike-share users previously commuted by car",
            "the decline in rush-hour travel times is not due entirely to factors unrelated to the bike-share program",
            "rush-hour travel times in neighboring cities did not decline during the same two-year period",
            "the bike-share program has attracted more members than city planners originally projected",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Necessary Assumption question - negate each candidate "
            "and keep the one whose negation breaks the argument.\n\n"
            "The editorial infers causation (the program reduced congestion) "
            "from sequence and correlation (times fell after launch). Any "
            "such argument depends on the effect not being wholly "
            "attributable to something else.\n\n"
            "(C) Negated: 'The decline IS due entirely to factors unrelated "
            "to the bike-share program' - a fuel-price spike, an employer "
            "moving out of downtown, a road widening. Then the program "
            "contributed nothing, and the conclusion has no support. The "
            "argument collapses, so (C) is necessary and correct. Note how "
            "weakly it is phrased: 'not due entirely to' is exactly the "
            "hedge a necessary assumption needs.\n\n"
            "(A) Negated: the city took other congestion measures too. The "
            "argument survives - bike-share can still deserve part of the "
            "credit. Too strong to be necessary.\n"
            "(B) Negated: most users did not previously drive. Even so, a "
            "substantial minority might have, which could be enough to move "
            "travel times. The word 'most' makes this stronger than the "
            "argument needs.\n"
            "(D) Negated: neighboring cities' times also fell. This suggests "
            "a regional cause and weakens the argument, but weakening is not "
            "the same as destroying - the program could still have "
            "contributed locally. Not necessary.\n"
            "(E) Negated: membership fell short of projections. Whether "
            "membership beat a forecast says nothing about whether the "
            "program affected congestion.\n\n"
            "Only (C)'s negation destroys the argument, so (C) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "flaw",
        "content_area": None,
        "stimulus": (
            "Columnist: The mayor claims that her proposed infrastructure "
            "plan will create thousands of jobs. But the mayor spent two "
            "decades as a construction executive and still owns shares in "
            "several construction firms that would bid on the resulting "
            "contracts. Her plan clearly will not create the jobs she "
            "promises."
        ),
        "question_stem": (
            "The reasoning in the columnist's argument is most vulnerable to "
            "criticism on the grounds that it"
        ),
        "choices": [
            "treats the fact that a claim was made by someone with a personal stake in it as sufficient grounds for concluding that the claim is false",
            "takes for granted that infrastructure spending is the only means by which a city can create jobs",
            "confuses a condition sufficient for job creation with one that is necessary for it",
            "draws a conclusion about the plan's total effect from evidence concerning only one industry",
            "assumes that what is true of the construction firms individually must be true of the construction industry as a whole",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Flaw question, so the answer must name the error "
            "using the recognized taxonomy rather than gesture at it.\n\n"
            "The columnist gives no evidence at all about the plan's likely "
            "employment effects. The entire case against the claim is the "
            "mayor's background and financial interest. That is the "
            "circumstantial ad hominem: attacking the source's motives "
            "instead of the claim's merits. It is compounded here because "
            "the columnist concludes the claim is FALSE, when at most a "
            "conflict of interest is a reason to scrutinize a claim, never a "
            "reason to conclude its opposite. (A) states this precisely.\n\n"
            "(B) The columnist never says or needs that infrastructure is "
            "the only route to job creation; that claim appears nowhere in "
            "the argument.\n"
            "(C) No conditional reasoning occurs here - there is no "
            "necessary/sufficient confusion to point to.\n"
            "(D) Misdescribes the structure: the columnist offers no "
            "industry evidence whatsoever, so the problem is not that the "
            "evidence base is too narrow, it is that there is none.\n"
            "(E) This names the fallacy of composition, which would require "
            "reasoning from parts to a whole. The columnist does not reason "
            "from individual firms to the industry.\n\n"
            "Only (A) names the flaw actually committed, so (A) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "flaw",
        "content_area": None,
        "stimulus": (
            "Letter to the editor: Everyone has a right to express their "
            "opinions. So when this newspaper declined to print my letter "
            "criticizing the school board, it violated my right to express "
            "my opinion. A newspaper that violates its readers' rights has "
            "no business calling itself a defender of free speech."
        ),
        "question_stem": (
            "The argument is most vulnerable to criticism on the grounds "
            "that it"
        ),
        "choices": [
            "generalizes from a single instance to a sweeping claim about the newspaper's character",
            'presupposes the very conclusion about the newspaper that it purports to establish',
            "assumes without any argument that the writer's criticism of the school board was substantially accurate",
            "relies on a key term that shifts meaning between a freedom from interference and a claim on another's press",
            "offers no evidence that the newspaper has ever described itself as a defender of free speech",
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Flaw question, so the answer must name the specific "
            "error from the taxonomy.\n\n"
            "The argument turns on 'right to express one's opinions.' In the "
            "first sentence that phrase carries its ordinary sense: a "
            "liberty to speak without being silenced by force or law. In the "
            "second sentence it is used in a quite different sense: a claim "
            "on someone else's printing press. A newspaper declining to "
            "print a letter does not stop the writer from expressing the "
            "opinion anywhere else. The argument only works if the two "
            "senses are treated as one, which is equivocation - a key term "
            "shifting meaning mid-argument. (D) names exactly this.\n\n"
            "(A) There is a generalization in the final sentence, but it "
            "follows from the rights claim; if the equivocation were "
            "repaired the inference would go through. The equivocation is "
            "the load-bearing error.\n"
            "(C) The accuracy of the criticism is irrelevant - the argument "
            "concerns the right to publish it, not its truth.\n"
            "(B) Circular reasoning would require the conclusion to appear "
            "among the premises. It does not; the premises are a rights "
            "claim and a factual claim about the newspaper's conduct.\n"
            "(E) A quibble about an unstated premise, not the reasoning "
            "error - and the argument's conditional final sentence does not "
            "require that the paper actually made that claim.\n\n"
            "Only (D) names the flaw actually committed, so (D) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "parallel_reasoning",
        "content_area": None,
        "stimulus": (
            "Every employee who completed the safety course received a "
            "certificate. Dana did not receive a certificate. Therefore Dana "
            "did not complete the safety course."
        ),
        "question_stem": (
            "Which one of the following arguments is most similar in its "
            "logical structure to the argument above?"
        ),
        "choices": [
            "All of the cottages that were repainted last summer have blue shutters. The Hendricks cottage does not have blue shutters. So the Hendricks cottage was not repainted last summer.",
            "Every student who submitted a portfolio was admitted to the program. Rafael submitted a portfolio. So Rafael was admitted to the program.",
            "All of the restaurants on Mill Street serve breakfast. The Copper Kettle serves breakfast. So the Copper Kettle is on Mill Street.",
            "Every bridge inspected this year passed inspection. The Halsey Bridge was not inspected this year. So the Halsey Bridge did not pass inspection.",
            "If a manuscript is accepted, it is sent to a copyeditor. If a manuscript is sent to a copyeditor, it is scheduled for publication. This manuscript was accepted. So it is scheduled for publication.",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Parallel Reasoning question, so abstract the original "
            "into its logical skeleton and match that form - not its "
            "subject matter.\n\n"
            "Original: let P = 'completed the safety course', Q = 'received "
            "a certificate'. The premises are P -> Q and not-Q, and the "
            "conclusion is not-P. That is modus tollens, a single valid "
            "conditional applied in the contrapositive direction.\n\n"
            "(A): P = 'repainted last summer', Q = 'has blue shutters'. "
            "P -> Q, not-Q, therefore not-P. Identical form, identically "
            "valid. This is the match.\n\n"
            "(B): P -> Q, P, therefore Q - modus ponens. Valid, but the "
            "wrong direction; it affirms the antecedent rather than denying "
            "the consequent.\n"
            "(C): P -> Q, Q, therefore P - affirming the consequent, an "
            "invalid form. The original is valid, so this cannot match.\n"
            "(D): P -> Q, not-P, therefore not-Q - denying the antecedent, "
            "also invalid. This is the trap for test takers who register "
            "'a negated premise' without checking which term is negated.\n"
            "(E): P -> Q, Q -> R, P, therefore R - a two-link chain, longer "
            "than the original's single conditional.\n\n"
            "Only (A) reproduces the original's exact modus tollens "
            "structure, so (A) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "parallel_reasoning",
        "content_area": None,
        "stimulus": (
            "Some of the volunteers at the shelter are certified first "
            "responders. Every certified first responder has completed CPR "
            "training. Therefore, some of the volunteers at the shelter have "
            "completed CPR training."
        ),
        "question_stem": (
            "The pattern of reasoning in which one of the following is most "
            "closely parallel to that in the argument above?"
        ),
        "choices": [
            "Some of the artifacts in the collection are Roman. Every Roman artifact in the collection has been catalogued. Therefore, some of the artifacts in the collection have been catalogued.",
            "Some of the trees in the orchard are pear trees. Every pear tree in the orchard was planted before 1990. Therefore, every tree in the orchard planted before 1990 is a pear tree.",
            "Some of the applicants hold graduate degrees. Some of the applicants have overseas experience. Therefore, some of the applicants hold graduate degrees and have overseas experience.",
            "Every member of the quartet studied at the conservatory. Some conservatory graduates teach privately. Therefore, some members of the quartet teach privately.",
            "If a painting is a forgery, it will fail spectroscopic analysis. This painting failed spectroscopic analysis. Therefore, this painting is a forgery.",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Parallel Reasoning question: abstract the form and "
            "match it, ignoring subject matter.\n\n"
            "Original: let A = volunteers, B = certified first responders, "
            "C = people who completed CPR training. The premises are 'Some A "
            "are B' and 'All B are C', and the conclusion is 'Some A are C'. "
            "This is a valid categorical syllogism - the existing overlap "
            "between A and B is carried into C by the universal premise.\n\n"
            "(A): A = artifacts, B = Roman artifacts, C = catalogued items. "
            "'Some A are B', 'All B are C', therefore 'Some A are C'. "
            "Identical form, identically valid. This is the match.\n\n"
            "(B): Premises of the same shape, but the conclusion reverses "
            "the relation into 'All C are B' - an illicit conversion, and "
            "invalid. The original's conclusion is an existential claim, not "
            "a universal one.\n"
            "(C): 'Some A are B', 'Some A are C', therefore 'Some A are both' "
            "- invalid; two separate overlaps need not coincide.\n"
            "(D): 'All A are B', 'Some B are C', therefore 'Some A are C' - "
            "invalid, because the Bs that are C need not be the Bs that are "
            "A. This is the closest trap: it uses the same two quantifiers "
            "as the original but attaches them to the wrong premises.\n"
            "(E): A conditional argument affirming the consequent - a "
            "different logical apparatus entirely, and invalid.\n\n"
            "Only (A) reproduces the original's exact valid structure, so "
            "(A) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "sufficient_assumption",
        "content_area": None,
        "stimulus": (
            "Service manager: Any technician who has completed the advanced "
            "certification can service our hybrid vehicles. Whitcomb, one of "
            "our technicians, has completed the advanced certification. So "
            "Whitcomb should be "
            "assigned to the hybrid service bay."
        ),
        "question_stem": (
            "The manager's conclusion follows logically if which one of the "
            "following is assumed?"
        ),
        "choices": [
            "Only technicians who have completed the advanced certification should be assigned to the hybrid service bay.",
            "Whitcomb has more experience with hybrid vehicles than any other technician at the shop.",
            "Most technicians who can service hybrid vehicles have completed the advanced certification.",
            "Any technician assigned to the hybrid service bay can service hybrid vehicles.",
            "Any technician who can service hybrid vehicles should be assigned to the hybrid service bay.",
        ],
        "correct_answer": "E",
        "explanation": (
            "This is a Sufficient Assumption question: the correct answer "
            "must close the premise-to-conclusion gap so completely that the "
            "conclusion follows with certainty.\n\n"
            "Let C = 'has completed the advanced certification', S = 'can "
            "service hybrid vehicles', A = 'should be assigned to the hybrid "
            "service bay'. Premises: C -> S, and C(Whitcomb). By modus "
            "ponens, S(Whitcomb). The conclusion is A(Whitcomb). Nothing "
            "given links S to A - that is precisely the gap.\n\n"
            "(E) supplies S -> A. Combined with S(Whitcomb), it yields "
            "A(Whitcomb) by modus ponens. The conclusion now follows with "
            "certainty, so (E) is correct.\n\n"
            "(A) supplies A -> C (only certified technicians should be "
            "assigned). That is the converse direction: it tells us who may "
            "NOT be assigned, never that anyone must be. Whitcomb's "
            "certification satisfies a necessary condition, which never "
            "guarantees the outcome. This is the most common trap on "
            "sufficient assumption questions.\n"
            "(C) 'Most' cannot generate a guaranteed conclusion about one "
            "individual; and it runs S -> C, the wrong direction as well.\n"
            "(D) supplies A -> S, again the converse of what is needed.\n"
            "(B) A comparative fact about experience, with no conditional "
            "force at all - it cannot make a conclusion follow logically.\n\n"
            "Only (E) makes the conclusion follow, so (E) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "sufficient_assumption",
        "content_area": None,
        "stimulus": (
            "Reporter: The council will approve the stadium bond only if the "
            "downtown business association supports it. This morning the "
            "association announced its support. So the bond will be "
            "approved."
        ),
        "question_stem": (
            "The reporter's conclusion follows logically if which one of the "
            "following is assumed?"
        ),
        "choices": [
            "The council approves most of the measures that the downtown business association supports.",
            "The downtown business association would not have announced its support unless it expected the bond to pass.",
            "If the downtown business association supports the stadium bond, the council will approve it.",
            "The council will not approve the stadium bond unless the association's support is unanimous.",
            "No measure opposed by the downtown business association has ever been approved by the council.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Sufficient Assumption question, so translate the "
            "conditionals precisely and find the answer that makes the "
            "conclusion airtight.\n\n"
            "'Only if' introduces a necessary condition. Let A = 'the "
            "council approves the bond', S = 'the association supports it'. "
            "The premise is A -> S, not S -> A. The other premise is S. From "
            "A -> S and S, nothing about A follows - inferring A here is "
            "affirming the consequent, a classic invalid move. The gap is "
            "the missing conditional in the other direction.\n\n"
            "(C) supplies exactly S -> A. With S already given, modus ponens "
            "yields A. The conclusion now follows with certainty, so (C) is "
            "correct.\n\n"
            "(A) 'Most' leaves room for this bond to be an exception, so the "
            "conclusion is not guaranteed. Sufficient assumption answers "
            "cannot be probabilistic.\n"
            "(B) Concerns the association's expectations and motives. Even "
            "if it expected passage, expectation does not entail approval.\n"
            "(D) Adds a second necessary condition. This makes approval "
            "harder to establish, not easier - it moves in the wrong "
            "direction entirely.\n"
            "(E) Restates a consequence of the original necessary condition "
            "(roughly its contrapositive) and so adds nothing new. Since the "
            "original premise was already insufficient, restating it leaves "
            "the gap exactly where it was.\n\n"
            "Only (C) makes the conclusion follow, so (C) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "strengthen",
        "content_area": None,
        "stimulus": (
            "Archaeologists have determined that a settlement in the "
            "Anatolian highlands was abandoned around 1200 BCE. Pollen "
            "samples taken from the site show a sharp decline in cultivated "
            "grain species during the same period. The archaeologists "
            "conclude that a prolonged drought forced the settlement's "
            "inhabitants to leave."
        ),
        "question_stem": (
            "Which one of the following, if true, most strengthens the "
            "archaeologists' conclusion?"
        ),
        "choices": [
            "Several other settlements in the Anatolian highlands were also abandoned during the twelfth century BCE.",
            "Weapons and burned structures characteristic of armed conflict have been found in the settlement's uppermost occupation layer.",
            "The settlement's inhabitants cultivated barley and emmer wheat, both of which require substantial rainfall.",
            "Sediment cores from a lake twenty kilometers from the settlement indicate that water levels there fell sharply between 1250 and 1150 BCE.",
            "Pollen analysis is the most widely used method for reconstructing ancient agricultural practices.",
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Strengthen question. The argument moves from an "
            "observation (grain pollen declined as the site was abandoned) "
            "to a specific causal explanation (drought). The strongest "
            "strengthener supplies independent evidence that the proposed "
            "cause was actually present.\n\n"
            "(D) does exactly that. Falling lake levels nearby over the same "
            "century are a direct climatic signal, gathered independently of "
            "the pollen record. Without it, the drought is only inferred "
            "from the very fact it is meant to explain; with it, the causal "
            "story gains outside corroboration. This is the correct "
            "answer.\n\n"
            "(A) Regional abandonment is consistent with drought, but "
            "equally consistent with invasion, disease, or trade collapse. "
            "It broadens the puzzle without favoring this explanation - the "
            "most tempting wrong answer here.\n"
            "(C) Establishes that the crops were rain-dependent, which makes "
            "drought a coherent mechanism, but offers no evidence that a "
            "drought occurred. It supports the link's plausibility, not its "
            "actuality, so it is weaker support than (D).\n"
            "(B) Supplies a competing explanation - armed conflict - and so "
            "weakens the argument rather than strengthening it.\n"
            "(E) A methodological aside about pollen analysis generally; it "
            "bears on the reliability of the observation, not on why the "
            "settlement was abandoned.\n\n"
            "(D) most strengthens the conclusion, so (D) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "strengthen",
        "content_area": None,
        "stimulus": (
            "Two years ago, Fairhaven Hospital began requiring surgical "
            "teams to complete a verification checklist before every "
            "operation. Post-surgical infection rates at the hospital have "
            "fallen by a third since then. Hospital administrators credit "
            "the checklist for the decline."
        ),
        "question_stem": (
            "Which one of the following, if true, most strengthens the "
            "administrators' claim?"
        ),
        "choices": [
            'Comparable hospitals in the region that adopted no checklist recorded no change in infection rates over the same period.',
            "The verification checklist costs the hospital very little to administer relative to the expense of treating a post-surgical infection.",
            "Surveys show that most of Fairhaven's surgical staff believe the checklist has improved communication in the operating room.",
            "Fairhaven Hospital adopted a new perioperative antibiotic protocol at the same time it introduced the checklist.",
            'Post-surgical infections are among the most common and most costly complications following major surgery of any kind.',
        ],
        "correct_answer": "A",
        "explanation": (
            "This is a Strengthen question. The administrators infer "
            "causation from a before-and-after correlation, so the argument "
            "depends on the decline not being the product of some broader "
            "trend that would have occurred anyway.\n\n"
            "(A) supplies the control group that the original evidence "
            "lacked. If similar hospitals without the checklist saw no "
            "change over the same window, a region-wide trend, a general "
            "improvement in surgical practice, or a coincidental drift are "
            "all ruled out as explanations, leaving the checklist as the "
            "salient difference. This is the strongest possible support "
            "short of a randomized trial, so (A) is correct.\n\n"
            "(B) Cost-effectiveness bears on whether the checklist is worth "
            "keeping, not on whether it caused the decline. Attractive "
            "because it sounds favorable, but it addresses a different "
            "question.\n"
            "(C) Staff belief is not evidence of effect; practitioners "
            "routinely believe in interventions that trials later find "
            "inert. It also names a plausible mechanism only in passing.\n"
            "(D) Introduces a confounding change made at the same time, "
            "which supplies a rival explanation and weakens the argument.\n"
            "(E) Establishes that the outcome matters, not that the "
            "checklist affected it.\n\n"
            "(A) most strengthens the claim, so (A) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "weaken",
        "content_area": None,
        "stimulus": (
            "Nutritionist: A large study found that adults who drink three "
            "or more cups of coffee daily have a 15 percent lower rate of "
            "type 2 diabetes than adults who drink none. Drinking coffee "
            "therefore helps protect against type 2 diabetes."
        ),
        "question_stem": (
            "Which one of the following, if true, most seriously weakens the "
            "nutritionist's argument?"
        ),
        "choices": [
            'The study did not distinguish between consumption of caffeinated and of decaffeinated coffee.',
            "Coffee contains chlorogenic acid, a compound shown in laboratory studies to affect glucose metabolism.",
            'Adults showing early metabolic warning signs of diabetes are routinely advised to cut back sharply on coffee.',
            'Some adults who drink no coffee at all nevertheless never go on to develop type 2 diabetes.',
            "The rate of type 2 diabetes among adults has risen in most countries over the past three decades.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Weaken question. The nutritionist infers causation "
            "(coffee protects) from a correlation (coffee drinkers have "
            "lower rates). Such an argument is most damaged by an "
            "explanation that accounts for the same correlation without the "
            "proposed cause.\n\n"
            "(C) supplies reverse causation. If people already trending "
            "toward diabetes are told to stop drinking coffee, then the "
            "non-drinker group is enriched with high-risk individuals "
            "precisely because they are high-risk. The correlation would "
            "appear even if coffee had no protective effect whatsoever - the "
            "arrow runs from incipient disease to abstention, not from "
            "coffee to protection. This guts the argument, so (C) is "
            "correct.\n\n"
            "(A) A limitation on what the study can attribute the effect to "
            "(caffeine vs. something else in coffee), but the conclusion is "
            "about coffee, not caffeine. It leaves the causal claim "
            "standing.\n"
            "(B) Supplies a plausible biological mechanism, which "
            "strengthens rather than weakens.\n"
            "(D) Irrelevant to a claim about rates. That some abstainers "
            "stay healthy is fully compatible with abstainers having a "
            "higher rate overall - a common trap that mistakes a statistical "
            "claim for a universal one.\n"
            "(E) A global trend affecting everyone does not explain the "
            "difference between the two groups within this study.\n\n"
            "Only (C) undermines the causal inference, so (C) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "weaken",
        "content_area": None,
        "stimulus": (
            "City planner: After we installed speed bumps on Elm Street last "
            "year, traffic accidents on that street fell by 40 percent. "
            "Installing speed bumps on every residential street in the city "
            "would produce a comparable reduction citywide."
        ),
        "question_stem": (
            "Which one of the following, if true, most seriously weakens the "
            "planner's argument?"
        ),
        "choices": [
            "Speed bumps modestly increase the response times of emergency vehicles.",
            "A new arterial road opened last year, diverting roughly half of Elm Street's former traffic volume onto another route.",
            "Elm Street residents report being satisfied with the speed bumps.",
            "Some residential streets in the city already have traffic-calming measures other than speed bumps.",
            "The city's total spending on road maintenance rose last year.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is a Weaken question. The planner's argument has two "
            "joints: that the speed bumps caused Elm Street's decline, and "
            "that the result would generalize citywide. The most serious "
            "weakener attacks the first, because if the speed bumps did not "
            "cause the drop, the recommendation loses its entire "
            "foundation.\n\n"
            "(B) does exactly that. If half of Elm Street's traffic "
            "disappeared onto a new road in the same year, then far fewer "
            "vehicles were present to collide, and the 40 percent decline is "
            "plausibly explained without the speed bumps doing any work at "
            "all. Extending an intervention whose effect was never "
            "demonstrated is unsupported, so (B) is correct.\n\n"
            "(A) Raises a genuine cost of speed bumps, but the conclusion is "
            "about reducing accidents, and this does not dispute that they "
            "would. A drawback is not a refutation of the causal claim - a "
            "frequent trap on weaken questions.\n"
            "(C) Resident satisfaction is irrelevant to accident causation.\n"
            "(D) Suggests some streets are already treated, which trims the "
            "policy's scope slightly but leaves the causal claim intact.\n"
            "(E) Total maintenance spending has no bearing on whether speed "
            "bumps reduce accidents.\n\n"
            "Only (B) undercuts the causal premise, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "inference",
        "content_area": None,
        "stimulus": (
            "Every grant application funded in this cycle included a "
            "detailed budget. No application submitted after the deadline "
            "included a detailed budget. Some applications submitted after "
            "the deadline were nevertheless reviewed by the committee."
        ),
        "question_stem": (
            "If the statements above are true, which one of the following "
            "must also be true?"
        ),
        "choices": [
            "No application submitted after the deadline was funded in this cycle.",
            "Some applications that included a detailed budget were submitted after the deadline.",
            "Every application that included a detailed budget was funded in this cycle.",
            "No application submitted after the deadline was reviewed by the committee.",
            "Some applications funded in this cycle were not reviewed by the committee.",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is an Inference (must-be-true) question, so the answer "
            "must follow by strict entailment - no plausible additions.\n\n"
            "Let F = funded this cycle, D = included a detailed budget, "
            "L = submitted after the deadline. The premises are F -> D, "
            "L -> not-D, and 'some L were reviewed'.\n\n"
            "Chain the first two by contraposition. From L -> not-D and "
            "F -> D: if an application is late, it lacks a detailed budget; "
            "if it lacks a detailed budget, it cannot be funded (the "
            "contrapositive of F -> D is not-D -> not-F). So L -> not-F: no "
            "late application was funded. That is (A), and it follows with "
            "certainty.\n\n"
            "(B) Directly contradicts L -> not-D. It cannot be true, let "
            "alone must be.\n"
            "(C) Reverses F -> D into D -> F. Affirming the consequent; a "
            "detailed budget was required for funding, not sufficient for "
            "it.\n"
            "(D) Contradicts the third premise, which states that some late "
            "applications WERE reviewed.\n"
            "(E) Nothing in the premises connects funding to review. The "
            "third premise tells us about some late applications only, and "
            "we already know none of those were funded - so no funded "
            "application is described either way.\n\n"
            "Only (A) is strictly entailed, so (A) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "inference",
        "content_area": None,
        "stimulus": (
            "The museum will display either the Kandinsky or the Malevich "
            "this season, but not both. If the Malevich is displayed, the "
            "east gallery will have to be closed for reinstallation. The "
            "east gallery will remain open throughout the season."
        ),
        "question_stem": (
            "If the statements above are true, which one of the following "
            "must also be true?"
        ),
        "choices": [
            "The Malevich will be placed in storage for the season.",
            "The Kandinsky will be displayed this season.",
            "If the east gallery were closed this season, the Malevich would be displayed.",
            "The east gallery is the only gallery large enough to house the Malevich.",
            "The museum has displayed the Kandinsky in a previous season.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an Inference question, so work the conditionals "
            "strictly.\n\n"
            "Let K = the Kandinsky is displayed, M = the Malevich is "
            "displayed, C = the east gallery is closed. The premises are: "
            "exactly one of K and M; M -> C; and not-C.\n\n"
            "From M -> C and not-C, modus tollens gives not-M. Since exactly "
            "one of the two will be displayed, and it is not the Malevich, "
            "it must be the Kandinsky: K. That is (B).\n\n"
            "(A) Not displaying the Malevich does not entail storing it. It "
            "might be lent out, kept in a study room, or hung elsewhere. "
            "This is the trap of importing a real-world default the premises "
            "never state.\n"
            "(C) Reverses the conditional. The premise is M -> C; (C) "
            "asserts C -> M. Nothing says the east gallery closes ONLY for "
            "the Malevich - it might close for a roof repair - so the "
            "converse does not follow. Note that a choice reading 'if the "
            "Kandinsky were not displayed, the gallery would be closed' "
            "would be a defective answer here, because the exclusive "
            "disjunction makes not-K entail M, and M entails closure; that "
            "version is genuinely derivable and would give the question two "
            "correct answers.\n"
            "(D) Offers an explanation for why the Malevich requires the "
            "east gallery. Explanations of the premises are not entailed by "
            "them.\n"
            "(E) The passage says nothing whatever about previous "
            "seasons.\n\n"
            "Only (B) follows from the premises, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "main_point",
        "content_area": None,
        "stimulus": (
            "Critics of remote work argue that it erodes the informal "
            "mentoring on which junior employees depend. The concern "
            "deserves a hearing, but it does not justify a blanket "
            "return-to-office mandate. Firms that have invested in "
            "structured mentoring programs report that their junior staff "
            "now receive more feedback, and more usable feedback, than they "
            "did when everyone shared a floor. Those same firms report lower "
            "attrition among employees under thirty. Informal hallway "
            "conversation, it turns out, was never an especially reliable "
            "way to transmit expertise."
        ),
        "question_stem": (
            "Which one of the following most accurately expresses the main "
            "conclusion of the argument?"
        ),
        "choices": [
            "Informal hallway conversation was never an especially reliable way to transmit expertise.",
            "Firms with structured mentoring programs report lower attrition among their youngest employees.",
            "The concern that remote work erodes informal mentoring does not justify requiring all employees to return to the office.",
            "Structured mentoring programs deliver more feedback to junior employees than shared office space does.",
            "Critics of remote work have generally failed to consider the evidence on employee attrition.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Main Point question, so locate the claim that "
            "everything else is offered to support - not the most striking "
            "or the last sentence.\n\n"
            "Structurally: sentence 1 states the critics' position "
            "(background). Sentence 2 concedes it partially and then "
            "delivers the author's own verdict - 'it does not justify a "
            "blanket return-to-office mandate.' Sentences 3 through 5 are "
            "evidence for that verdict: more feedback, lower attrition, and "
            "an explanation of why the old arrangement was overrated. The "
            "'but' in sentence 2 is the structural signal that what follows "
            "it is the author's claim. (C) restates that verdict.\n\n"
            "(A) Is the final sentence, and final sentences are the classic "
            "main-point trap. Here it functions as an explanation supporting "
            "the verdict, not as the verdict itself.\n"
            "(B) A reported finding offered as evidence.\n"
            "(D) Another reported finding offered as evidence.\n"
            "(E) Never asserted. The author engages the critics' concern "
            "rather than accusing them of ignoring data.\n\n"
            "Only (C) is the conclusion the rest supports, so (C) is "
            "correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "main_point",
        "content_area": None,
        "stimulus": (
            "Some economists are urging the central bank to raise interest "
            "rates further to ensure that inflation returns to its target. "
            "This advice is unwise. Inflation has already declined for six "
            "consecutive quarters, and the full effect of an interest rate "
            "increase takes up to two years to register in the data. Raising "
            "rates now would compound tightening whose effects have not yet "
            "been felt."
        ),
        "question_stem": (
            "Which one of the following most accurately expresses the main "
            "point of the argument?"
        ),
        "choices": [
            "Inflation has declined for six consecutive quarters.",
            "Economists disagree about how quickly interest rate changes affect inflation.",
            "The full effect of an interest rate increase can take as long as two years to appear in economic data.",
            "Inflation will return to the central bank's target without any further action.",
            "The central bank should not raise interest rates further at this time.",
        ],
        "correct_answer": "E",
        "explanation": (
            "This is a Main Point question: find the claim the other "
            "sentences are marshalled to support.\n\n"
            "Sentence 1 reports the economists' recommendation "
            "(background). Sentence 2 - 'This advice is unwise' - is the "
            "author's verdict on it. Sentences 3 and 4 supply the reasons: "
            "inflation is already falling, policy acts with a long lag, and "
            "acting now would stack tightening on tightening. Restating the "
            "verdict in substantive terms gives (E): the bank should not "
            "raise rates further now.\n\n"
            "(A) A premise, offered as evidence for the verdict.\n"
            "(C) Also a premise - the lag claim is the reason compounding "
            "is a danger.\n"
            "(D) Overstates. The argument says further raising is unwise, "
            "which is compatible with inflation needing other measures, or "
            "with some uncertainty about the path. Arguing against an action "
            "is not predicting a particular outcome.\n"
            "(B) Never claimed. Only one side's view is described, and the "
            "author's disagreement with it is not a report about the "
            "profession.\n\n"
            "Only (E) is the conclusion the premises support, so (E) is "
            "correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "method_of_reasoning",
        "content_area": None,
        "stimulus": (
            "Historian: Several scholars maintain that the printing press "
            "caused the Reformation. But presses had operated across Europe "
            "for more than fifty years before Luther circulated his theses, "
            "and in that period they turned out mostly devotional books and "
            "legal forms. A technology that sat available and unused for two "
            "generations is not the cause of an upheaval that finally "
            "arrived; at most it was a condition that made the upheaval "
            "possible once other causes were in place."
        ),
        "question_stem": (
            "The historian's argument proceeds by"
        ),
        "choices": [
            "attacking the scholars' competence and motives rather than the substance of the claim they defend",
            "arguing that the scholars' position, carried to its conclusion, leads to an outright self-contradiction",
            'citing a single counterexample in order to refute a broad universal generalization',
            'distinguishing a cause of an event from a condition that merely made the event possible',
            'appealing to the settled consensus of professional historians in order to resolve a disputed question',
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Method of Reasoning question, so describe the "
            "technique abstractly, independent of the subject matter.\n\n"
            "The historian does not deny that presses mattered. The move is "
            "to introduce a conceptual distinction - between a cause and an "
            "enabling condition - and then argue, from the fifty-year gap "
            "between availability and effect, that the press belongs on the "
            "enabling-condition side. The final clause states the "
            "reclassification explicitly: 'at most it was a condition that "
            "made the upheaval possible.' (D) describes exactly this.\n\n"
            "(A) No remark is made about the scholars themselves; the "
            "argument engages their claim directly.\n"
            "(C) The fifty-year gap is evidence, not a counterexample to a "
            "universal generalization - and the scholars' claim is causal, "
            "not universal, so there is no 'all' statement to refute.\n"
            "(B) The historian never claims the opposing view contradicts "
            "itself, only that it misclassifies the press's role.\n"
            "(E) No appeal to consensus appears; if anything the historian "
            "argues against several scholars.\n\n"
            "Only (D) names the method used, so (D) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "method_of_reasoning",
        "content_area": None,
        "stimulus": (
            "Attorney: Opposing counsel argues that my client cannot have "
            "been at the warehouse on the night of the fire, because a "
            "traffic camera photographed his car downtown at 11:40. But the "
            "warehouse is a twelve-minute drive from that intersection, and "
            "the fire was not reported until 12:30. The photograph is "
            "therefore no obstacle to placing my client at the warehouse."
        ),
        "question_stem": (
            "The attorney's argument proceeds by"
        ),
        "choices": [
            "presenting evidence that a witness for the opposing side is unreliable",
            "showing that evidence offered to rule out a possibility is in fact compatible with that possibility",
            "conceding a claim while arguing that it has been given undue weight",
            "identifying an alternative suspect who had both motive and opportunity",
            "arguing that the opposing side's conclusion rests on an unrepresentative sample",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is a Method of Reasoning question: name the abstract "
            "technique.\n\n"
            "Opposing counsel treats the 11:40 photograph as excluding the "
            "client from the warehouse. The attorney does not dispute the "
            "photograph, question the camera, or blame anyone else. Instead "
            "the attorney does arithmetic on it: 11:40 plus a twelve-minute "
            "drive is 11:52, comfortably before the 12:30 alarm. The very "
            "evidence offered to establish impossibility turns out to leave "
            "the possibility open. (B) captures this precisely.\n\n"
            "(A) No witness's reliability is challenged; the photograph is "
            "accepted as accurate.\n"
            "(C) Close, and the most tempting wrong answer - the attorney "
            "does concede the photograph. But the argument is not that it "
            "has been overweighted; it is that, properly read, it does not "
            "support the opposing inference at all. That is a stronger and "
            "different move.\n"
            "(D) No alternative suspect is mentioned.\n"
            "(E) No sampling or generalization is involved.\n\n"
            "Only (B) names the method used, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "principle",
        "content_area": None,
        "stimulus": (
            "A restaurant critic accepted a complimentary tasting menu from "
            "a restaurant and, three weeks later, published a highly "
            "favorable review of it without mentioning the free meal. Her "
            "editor concluded that she had acted improperly, even though the "
            "critic maintains, and the editor accepts, that the meal had no "
            "influence on her assessment."
        ),
        "question_stem": (
            "Which one of the following principles, if valid, most helps to "
            "justify the editor's conclusion?"
        ),
        "choices": [
            'A reviewer should decline any hospitality whose value exceeds what an ordinary reader of the publication could comfortably afford to pay.',
            'A published review is improper if the opinions it expresses are not sincerely held by the critic who signed her name to it.',
            'A journalist acts improperly by accepting something of value from a subject and not disclosing it, whether or not judgment was affected.',
            'A publication should assign reviewers only to subjects with which they have had no prior dealings, whether social or financial.',
            'A journalist whose judgment has actually been influenced by a gift should recuse herself from covering the person who gave it.',
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Principle-Justify question: the correct answer is a "
            "general rule that, applied to these facts, yields the specific "
            "judgment reached.\n\n"
            "The facts to be justified are unusual in one respect: the "
            "editor accepts that the critic's judgment was NOT affected, yet "
            "still finds impropriety. So the justifying principle must make "
            "the impropriety turn on something other than actual influence - "
            "namely on the undisclosed acceptance itself.\n\n"
            "(C) does this exactly, and its final clause - 'whether or not "
            "judgment was affected' - is what makes it fit a case where "
            "influence is conceded to be absent. "
            "Applied here, the critic accepted something of value and did "
            "not disclose it, so she acted improperly. (C) is correct.\n\n"
            "(A) Turns on the meal's value, about which the stimulus says "
            "nothing, so it cannot be applied to these facts.\n"
            "(B) Requires insincerity. The editor accepts the review "
            "reflected the critic's real assessment, so this principle would "
            "find no impropriety - it argues against the conclusion.\n"
            "(D) Would bar the assignment before any meal occurred, and the "
            "stimulus reports no prior dealings; it does not reach the "
            "conduct actually at issue.\n"
            "(E) Conditions the duty on the journalist's having been "
            "influenced - expressly not the case here - so it too fails to "
            "justify the editor.\n\n"
            "Only (C) justifies the specific judgment, so (C) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "principle",
        "content_area": None,
        "stimulus": (
            "The forestry service granted a timber company permission to "
            "harvest a tract of old-growth forest after the company agreed "
            "to replant three times the area it would cut. Old-growth forest "
            "of this kind requires several centuries to develop its "
            "characteristic structure. An ecologist has argued that the "
            "forestry service acted wrongly in granting the permit."
        ),
        "question_stem": (
            "Which one of the following principles, if valid, most helps to "
            "justify the ecologist's position?"
        ),
        "choices": [
            "A public agency should grant permits only to companies that have complied with the terms of their previous permits.",
            'An agency should not authorize destroying a resource that cannot be restored within a human lifetime, whatever the compensation.',
            "Compensation for environmental damage should always exceed the value of what was damaged.",
            'A timber company should be required to replant any area of forest that it has been permitted to harvest.',
            'Decisions affecting publicly owned land should be made only after a formal opportunity for public comment.',
        ],
        "correct_answer": "B",
        "explanation": (
            "This is a Principle-Justify question, so find the rule that "
            "delivers the ecologist's specific verdict on these specific "
            "facts.\n\n"
            "The salient facts are that the resource takes centuries to "
            "regenerate and that compensation was offered and accepted as "
            "adequate in area. To condemn the permit, a principle must make "
            "the compensation irrelevant.\n\n"
            "(B) does so directly: irreplaceable-within-a-lifetime resources "
            "may not be authorized for destruction, 'whatever the "
            "compensation.' Old-growth structure takes centuries, so the tract "
            "qualifies, and the three-to-one replanting deal cannot cure the "
            "problem. The permit was therefore wrongly granted. (B) is "
            "correct.\n\n"
            "(A) Concerns the company's compliance history, on which the "
            "stimulus is silent - the principle cannot be applied.\n"
            "(C) Is the most tempting wrong answer, because it sounds "
            "demanding. But it endorses the compensation framework the "
            "ecologist must reject, and three times the area might well "
            "satisfy it - so it tends to justify the permit, not condemn "
            "it.\n"
            "(D) Was satisfied here, and then some. It supports the "
            "service's decision.\n"
            "(E) Raises a procedural requirement the stimulus never "
            "mentions, so nothing in these facts shows it was violated.\n\n"
            "Only (B) justifies the ecologist's position, so (B) is "
            "correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "resolve_explain",
        "content_area": None,
        "stimulus": (
            "In the decade following a sustained national campaign urging "
            "drivers to wear seat belts, the proportion of drivers who wore "
            "them rose from 30 percent to 80 percent. Seat belts are known "
            "to substantially reduce a driver's chance of dying in a given "
            "crash. Yet the total number of drivers killed in traffic "
            "accidents was no lower at the end of the decade than at the "
            "beginning."
        ),
        "question_stem": (
            "Which one of the following, if true, most helps to resolve the "
            "apparent discrepancy described above?"
        ),
        "choices": [
            "Seat belts reduce the severity of injuries in crashes that are not fatal as well as in those that are.",
            "Automobile manufacturers introduced side-impact airbags during the same decade.",
            "The national campaign was more effective in urban areas than in rural areas.",
            "Some drivers who wear seat belts fasten them incorrectly, reducing their effectiveness.",
            "The total number of miles driven nationally nearly doubled over the course of the decade.",
        ],
        "correct_answer": "E",
        "explanation": (
            "This is a Resolve/Explain question. The correct answer must "
            "supply a fact that lets every statement in the stimulus be true "
            "at once - here, that seat belt use rose sharply, that seat "
            "belts genuinely save lives, and that total deaths did not "
            "fall.\n\n"
            "(E) resolves it cleanly by separating the rate from the total. "
            "If exposure - miles driven - nearly doubled, then there were "
            "far more crashes to be killed in. A large drop in deaths per "
            "mile can leave the raw death count flat. Both the "
            "effectiveness claim and the disappointing headline number are "
            "true, and the tension dissolves. (E) is correct.\n\n"
            "(A) Adds another benefit of seat belts. This deepens the "
            "puzzle rather than resolving it: the more good seat belts do, "
            "the stranger a flat death count becomes.\n"
            "(C) A geographic difference in uptake, but the stimulus already "
            "grants that overall use rose to 80 percent nationally.\n"
            "(D) The most tempting wrong answer, since it chips at "
            "effectiveness. But 'some drivers' misfasten belts is far too "
            "small a qualification to absorb a 50-point rise in usage, and "
            "the stimulus stipulates belts substantially reduce fatality "
            "risk.\n"
            "(B) Another safety improvement, which like (A) should have "
            "pushed deaths down further, worsening the puzzle.\n\n"
            "Only (E) reconciles all the facts, so (E) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "resolve_explain",
        "content_area": None,
        "stimulus": (
            "One species of tropical orchid produces no nectar and offers "
            "visiting insects no nourishment of any kind. Producing a reward "
            "is generally thought necessary to secure repeat visits from "
            "pollinators. Yet this orchid is pollinated more reliably than "
            "neighboring orchid species that do produce abundant nectar."
        ),
        "question_stem": (
            "Which one of the following, if true, most helps to explain the "
            "orchid's pollination success?"
        ),
        "choices": [
            "The rewardless orchid produces far more flowers per plant than its nectar-producing neighbors do.",
            "The orchid's flowers mimic the appearance and scent of female wasps, causing male wasps to try to mate with them.",
            "Nectar production consumes energy that a plant could otherwise devote to seed development.",
            "The nectar-producing orchids in the area are visited by a wider variety of insect species.",
            'Tropical orchids generally depend on visiting insects rather than on wind currents for successful pollination.',
        ],
        "correct_answer": "B",
        "explanation": (
            "This is a Resolve/Explain question. The tension is that a "
            "reward is supposedly needed to attract pollinators, yet the "
            "rewardless species outperforms rewarding ones. The answer must "
            "show how pollination can be secured without a reward.\n\n"
            "(B) identifies an entirely different attraction mechanism: "
            "sexual deception. Male wasps are drawn by what appears to be a "
            "mate, not by food, so the absence of nectar costs the orchid "
            "nothing. It also explains the superior reliability - a male "
            "wasp pursuing mates visits many flowers of that one species, "
            "which delivers pollen precisely where it must go, whereas "
            "nectar feeders wander among species. Both facts are now "
            "consistent. (B) is correct.\n\n"
            "(A) More flowers might yield more total visits, but the puzzle "
            "is why insects come at all when there is no reward - the "
            "mechanism is left unexplained.\n"
            "(C) Explains why forgoing nectar might be advantageous once "
            "pollination is secured. It does not explain how pollination is "
            "secured, which is the actual discrepancy.\n"
            "(D) Deepens the puzzle: broader insect visitation to the "
            "rewarding species makes their worse pollination outcome more "
            "surprising, not less.\n"
            "(E) General background true of all the species involved, so it "
            "cannot explain a difference among them.\n\n"
            "Only (B) resolves the discrepancy, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "evaluate_argument",
        "content_area": None,
        "stimulus": (
            "District official: We should replace our printed textbooks with "
            "tablets. A tablet costs the district less than the six printed "
            "textbooks a student receives each year, so the switch will save "
            "money."
        ),
        "question_stem": (
            "The answer to which one of the following questions would be "
            "most useful in evaluating the official's argument?"
        ),
        "choices": [
            "For how many school years is a printed textbook typically used before the district replaces it?",
            "Do students in the district generally prefer reading on screens to reading on paper?",
            "Do all students in the district have reliable internet access at home?",
            "Have teachers in the district received training in the use of tablets?",
            "Does prolonged screen reading cause eye strain in adolescents?",
        ],
        "correct_answer": "A",
        "explanation": (
            "This is an Evaluate the Argument question: the right answer is "
            "the question whose answer would most affect whether the "
            "argument holds.\n\n"
            "The official compares the price of one tablet against six "
            "textbooks 'each year,' which quietly assumes those textbooks "
            "are a recurring annual cost. Printed textbooks, however, are "
            "normally reissued to successive students for years. If a book "
            "serves seven cohorts, its cost per student per year is a "
            "seventh of its price, and the comparison collapses. If books "
            "really are bought fresh annually, the comparison holds.\n\n"
            "(A) asks precisely this. A short lifespan supports the "
            "official; a long one undercuts the argument. Because the answer "
            "swings the conclusion in opposite directions, it is the most "
            "useful evaluative question, so (A) is correct.\n\n"
            "(B) Student preference bears on desirability, not on the cost "
            "claim the argument actually makes.\n"
            "(C) Home internet access matters for implementation and equity, "
            "and is the most tempting wrong answer, but the argument's claim "
            "is strictly financial.\n"
            "(D) Training costs would be relevant if the question asked "
            "about them, but as phrased it asks only whether training has "
            "occurred - and either answer leaves the textbook comparison "
            "untouched.\n"
            "(E) A health consideration, again not a test of the cost "
            "reasoning.\n\n"
            "Only (A) tests the argument's key assumption, so (A) is "
            "correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "evaluate_argument",
        "content_area": None,
        "stimulus": (
            "Airline executive: Our new boarding procedure is faster than "
            "the one it replaced. In the three months before the change, "
            "flights took an average of 24 minutes to board; in the three "
            "months after, the average was 19 minutes."
        ),
        "question_stem": (
            "It would be most useful to know which one of the following in "
            "evaluating the executive's argument?"
        ),
        "choices": [
            "Whether passengers reported greater satisfaction with the new boarding procedure",
            "Whether the aircraft operated in the two periods carried comparable numbers of passengers",
            "Whether the airline's competitors have adopted similar boarding procedures",
            "Whether gate agents required additional training to implement the new procedure",
            "Whether the airline's on-time departure rate improved after the change",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an Evaluate the Argument question. The executive treats "
            "a before-and-after difference in average boarding time as "
            "showing the procedure is faster, which assumes the two periods "
            "are otherwise comparable.\n\n"
            "Passenger count is the most obvious way that assumption could "
            "fail: boarding a 180-seat aircraft takes longer than boarding a "
            "70-seat one regardless of procedure. If the later period "
            "happened to run smaller or emptier aircraft - a seasonal "
            "schedule change, say - the five-minute improvement could be "
            "entirely an artifact of load rather than method.\n\n"
            "(B) asks exactly this, and its answer moves the conclusion both "
            "ways: comparable loads support the executive, divergent loads "
            "undercut the comparison. (B) is correct.\n\n"
            "(A) Satisfaction measures how boarding felt, not how long it "
            "took; the claim at issue is strictly about speed.\n"
            "(C) What competitors do says nothing about whether this "
            "procedure worked here.\n"
            "(D) Training effort bears on cost and difficulty of adoption, "
            "not on whether boarding became faster.\n"
            "(E) The most tempting wrong answer, since on-time departures "
            "sound like corroboration. But departure punctuality depends on "
            "crew scheduling, air traffic control, maintenance and turnaround "
            "as much as boarding, so either answer is consistent with the "
            "procedure having no effect.\n\n"
            "Only (B) tests the argument's comparability assumption, so (B) "
            "is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "point_at_issue",
        "content_area": None,
        "stimulus": (
            "Ravi: Museums holding artifacts acquired during the colonial "
            "period should return them to their countries of origin. These "
            "objects were taken under conditions no one today would call "
            "consensual.\n"
            "Lena: The acquisitions were indeed coercive. But many origin "
            "countries do not yet have storage and conservation facilities "
            "meeting international standards, and an artifact ruined by poor "
            "storage serves no one, least of all the community it came from. "
            "Return should wait until such facilities are in place."
        ),
        "question_stem": (
            "Ravi and Lena disagree with each other about whether"
        ),
        "choices": [
            'artifacts acquired by museums during the colonial period were originally obtained coercively',
            'the countries an artifact came from have a legitimate moral claim to its eventual return',
            "conservation standards for museum artifacts are set at an appropriate level",
            "returning colonial-era artifacts should depend on the receiving country's conservation capacity",
            'museums bear a genuine obligation to preserve the artifacts currently held in their collections',
        ],
        "correct_answer": "D",
        "explanation": (
            "This is a Point at Issue question. The answer must be a claim "
            "the two speakers would answer differently, and both positions "
            "must be supportable from the text - a topic only one speaker "
            "mentions cannot be the disagreement.\n\n"
            "Ravi calls for return, full stop, resting on the coercive "
            "acquisition. Lena grants the coercion, then argues that return "
            "'should wait until such facilities are in place.' Ravi's "
            "unconditional 'should return' and Lena's explicit precondition "
            "are directly opposed answers to the same question: does the "
            "obligation to return depend on the recipient's conservation "
            "capacity? (D) states it, so (D) is correct.\n\n"
            "(A) Expressly agreed. Lena opens by conceding 'the acquisitions "
            "were indeed coercive.' This is the classic trap of mistaking "
            "the shared premise for the dispute.\n"
            "(C) Neither speaker evaluates whether the standards themselves "
            "are pitched correctly; Lena treats them as a given.\n"
            "(B) Ravi clearly affirms it and Lena shows no sign of denying "
            "it - her objection is about timing and capacity, not "
            "entitlement.\n"
            "(E) Lena stresses preservation; Ravi never disputes that "
            "artifacts should be preserved, only who should hold them.\n\n"
            "Only (D) is a claim the two answer differently, so (D) is "
            "correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "point_at_issue",
        "content_area": None,
        "stimulus": (
            "Tomas: The city should fund the proposed light rail line. Over "
            "a thirty-year horizon it will move more passengers per dollar "
            "invested than any road project we could build instead.\n"
            "Wen: Thirty-year projections assume commuting patterns that "
            "remote work has already unsettled. We would do better to fund "
            "bus rapid transit, whose routes can be redrawn cheaply if "
            "demand shifts."
        ),
        "question_stem": (
            "Tomas and Wen disagree over whether"
        ),
        "choices": [
            "the city should invest public money in transit rather than in road projects",
            "the proposed light rail line is the transit investment the city should fund",
            "remote work has reduced the total number of commuting trips in the city",
            "bus rapid transit routes can be modified more cheaply than rail routes",
            "long-term projections are ever useful in evaluating infrastructure proposals",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is a Point at Issue question: identify the claim on which "
            "the two take opposite, textually supported positions.\n\n"
            "Tomas advocates funding the light rail line. Wen says the city "
            "'would do better to fund bus rapid transit,' which is a "
            "rejection of light rail as the right investment. That is a "
            "direct clash on a single question, captured by (B).\n\n"
            "(A) Both favor transit spending - Wen's alternative is itself a "
            "transit project, and neither argues for roads. Wen's mention of "
            "road projects appears only inside Tomas's comparison.\n"
            "(C) Wen says remote work has 'unsettled' commuting patterns, "
            "not that total trips have fallen, and Tomas takes no position "
            "on remote work at all. Nothing shows disagreement.\n"
            "(D) Wen asserts this and Tomas never contradicts it; an "
            "uncontested assertion is not a point at issue. This is the "
            "sharpest trap here, because the claim is what drives Wen's "
            "argument.\n"
            "(E) Wen questions these particular thirty-year projections, "
            "which is far short of denying that long-term projections are "
            "ever useful - the 'ever' overstates her position.\n\n"
            "Only (B) is a genuine disagreement, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "role_of_statement",
        "content_area": None,
        "stimulus": (
            "The experimental compound reduced tumor size in 60 percent of "
            "the patients enrolled in the trial. It did so, however, only at "
            "doses that produced severe liver toxicity in nearly half of "
            "them. A therapy that shrinks tumors while damaging the organ "
            "responsible for clearing it from the body is unlikely to extend "
            "patients' lives. The compound should not be approved in its "
            "current formulation."
        ),
        "question_stem": (
            "The claim that the compound reduced tumor size in 60 percent of "
            "the patients enrolled in the trial plays which one of the "
            "following roles in the argument?"
        ),
        "choices": [
            "It is the main conclusion the argument is designed to establish.",
            "It is evidence the argument offers in direct support of its conclusion about approval.",
            "It is a finding the argument accepts as accurate but contends is insufficient to support approval.",
            "It is a claim the argument attempts to show is based on an unrepresentative sample.",
            "It is an observation the argument dismisses as irrelevant to the compound's therapeutic value.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is a Role of a Statement question: describe the claim's "
            "structural function, not its content.\n\n"
            "The 60 percent figure is the strongest thing that can be said "
            "for the compound, and the argument never disputes it. It is "
            "introduced and then immediately qualified by 'however,' after "
            "which the toxicity finding and the survival reasoning carry the "
            "argument to its conclusion that the compound should not be "
            "approved. So the claim is a conceded favorable finding whose "
            "force the argument goes on to deny - (C).\n\n"
            "(A) The main conclusion is the final sentence about approval.\n"
            "(B) Reverses the claim's direction. Tumor reduction is evidence "
            "FOR the compound; the argument concludes against it. A "
            "concession is not a premise for the conclusion it cuts "
            "against - this is the most common error on role questions.\n"
            "(D) No challenge to the trial's sample is made anywhere; the "
            "data are taken at face value.\n"
            "(E) Too strong. The argument does not call tumor reduction "
            "irrelevant - it treats it as a real benefit that is outweighed "
            "by toxicity, which is a different and weaker claim than "
            "irrelevance.\n\n"
            "Only (C) captures the claim's role, so (C) is correct."
        ),
        "verified": True,
    },
    {
        "section": "logical_reasoning",
        "question_type": "role_of_statement",
        "content_area": None,
        "stimulus": (
            "Supporters of the proposed bag ban point out that similar bans "
            "in three neighboring counties reduced plastic litter by about "
            "40 percent. That figure is accurate. But each of those counties "
            "paired its ban with a program distributing free reusable bags "
            "to low-income households, and our proposal contains no such "
            "program. We should not expect a comparable reduction here."
        ),
        "question_stem": (
            "The statement that the 40 percent figure is accurate plays "
            "which one of the following roles in the argument?"
        ),
        "choices": [
            "It is a premise offered in direct support of the argument's main conclusion about the proposed ban.",
            'It is a claim that the argument goes on to demonstrate is false, using evidence from the neighboring counties.',
            'It is the main conclusion that the argument as a whole is designed to establish.',
            'It is an example offered to illustrate a general principle about policy transfer stated elsewhere in the argument.',
            "It is a concession that the opposing side's evidence is accurate, offered before explaining why it does not transfer.",
        ],
        "correct_answer": "E",
        "explanation": (
            "This is a Role of a Statement question, so identify the "
            "function of the sentence in the argument's structure.\n\n"
            "'That figure is accurate' does no work in support of the "
            "conclusion; it grants the opponents their data. The argument "
            "then pivots on 'But' to the disanalogy - the neighboring "
            "counties bundled free-bag programs that this proposal lacks - "
            "and concludes that a comparable reduction should not be "
            "expected. The sentence is therefore a concession, positioned "
            "before the reason the conceded evidence fails to transfer. That "
            "is (E).\n\n"
            "(A) A premise supports the conclusion. This statement, taken "
            "alone, cuts toward the opposite conclusion, which is exactly "
            "why the argument must neutralize it.\n"
            "(C) The main conclusion is the final sentence about not "
            "expecting comparable results.\n"
            "(D) No general principle is stated in the argument for this to "
            "illustrate.\n"
            "(B) The most tempting wrong answer, because the argument does "
            "resist the opponents' inference. But it never disputes the "
            "figure's truth - it explicitly affirms it and challenges only "
            "its applicability here.\n\n"
            "Only (E) captures the statement's role, so (E) is correct."
        ),
        "verified": True,
    },
]
