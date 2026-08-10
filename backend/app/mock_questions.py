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
            "The overall enrollment at Ridgeline Elementary has remained stable over the past two years.",
            "Several other elementary schools in the district have also reported decreases in cafeteria food waste this year.",
            "Ridgeline Elementary's cafeteria staff received training on portion control shortly before the schedule change.",
            "Students who have recess before lunch report feeling less rushed and hungrier when they sit down to eat than students who have recess after lunch.",
            "Students at Ridgeline Elementary have mixed opinions about whether they prefer recess before or after lunch.",
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
            "(A) is irrelevant: the 30 percent figure is already a "
            "proportion, so stable enrollment neither helps nor hurts the "
            "causal claim.\n"
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
            "The wellness program includes gym membership discounts and healthy-eating seminars.",
            "Employees who choose to participate in the optional wellness program tend to already prioritize their health and take fewer sick days than their colleagues, regardless of the program.",
            "Trenton Manufacturing has offered the wellness program for the past five years.",
            "Some employees who do not participate in the wellness program also take very few sick days.",
            "The wellness program costs the company a modest amount per participating employee each year.",
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
            "The criticism that co-ops' fee structure inherently excludes low-income residents is not well-supported by the evidence.",
            "Co-op membership in low-income neighborhoods has grown steadily over the past decade.",
            "Urban food co-ops are a complete solution to food access problems in low-income neighborhoods.",
            "Critics of urban food co-ops are mainly concerned with the co-ops' membership-fee model.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is a Main Point question, so the correct answer must be "
            "the argument's ultimate conclusion, identified via structural "
            "analysis - not a premise or sub-point offered in its support.\n\n"
            "The passage opens by presenting the critics' claim (background), "
            "then offers two premises (sliding-scale/waiver options; "
            "membership growth in low-income areas), and closes with 'the "
            "criticism ... is not well-supported by the evidence' - signaled "
            "as the takeaway by the concluding position after 'while co-ops "
            "are not a complete solution.' That closing claim, (B), is what "
            "the premises are marshalled to support.\n\n"
            "(A) and (C) are each one of the two premises offered in support "
            "of (B), not the conclusion itself.\n"
            "(D) misstates the argument, which explicitly denies co-ops are "
            "a complete solution.\n"
            "(E) describes the critics' concern, not the author's own "
            "concluding claim.\n\n"
            "Only (B) is the ultimate conclusion, so (B) is correct."
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
            "A business should only be fined for ordinance violations if the violation was intentional.",
            "Noise ordinances should apply equally to daytime and nighttime operations.",
            "A business should be fined for violating an ordinance if its operations exceed the ordinance's limits during any period the ordinance covers, even if the business complies during other periods.",
            "A business that complies with an ordinance for the majority of its operating hours should not be fined.",
            "Fines for noise ordinance violations should be proportional to the number of residents affected.",
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
            "Glycogen depletion is the most common cause of slowing in the final miles of a marathon.",
            "The winning runner has won several marathons in the past.",
            "The Cedar City Marathon course is relatively flat compared to other marathon courses.",
            "The winning runner deliberately ran the first six miles at a slower, more conservative pace than her natural race pace, saving her energy for a faster finish.",
            "Average finishers in the Cedar City Marathon consumed sports drinks during the race.",
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
            "to reduce collisions at similarly designed intersections in "
            "other cities.\" The city council should approve funding for "
            "this project."
        ),
        "question_stem": "The answer to which one of the following questions would be most useful in evaluating the city planner's argument?",
        "choices": [
            "How much will it cost the city to install roundabouts at the three intersections?",
            "Are the three accident-prone intersections in Millbrook similar in traffic volume and geometry to the intersections in other cities where roundabouts reduced collisions?",
            "How long has Millbrook's city council been discussing traffic safety improvements?",
            "Do most drivers in Millbrook support the installation of roundabouts?",
            "Have other cities that installed roundabouts also made other traffic safety improvements at the same time?",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an Evaluate the Argument question, so the correct "
            "answer must be a question whose answer would reveal whether the "
            "argument's central assumption actually holds.\n\n"
            "The argument relies on an analogy: because roundabouts reduced "
            "collisions at 'similarly designed intersections in other "
            "cities,' they will do the same in Millbrook. The central "
            "assumption is that Millbrook's intersections are, in fact, "
            "comparable to those other intersections. (B) asks exactly this "
            "- a 'no' answer would seriously undermine the argument, a "
            "'yes' would support it.\n\n"
            "(A) bears on whether funding the project is worthwhile, not on "
            "whether the roundabouts would actually reduce collisions - a "
            "different question from the one the argument is making.\n"
            "(C) is irrelevant to whether roundabouts would work.\n"
            "(D) driver opinion doesn't bear on whether collisions would "
            "actually decrease.\n"
            "(E) touches on a possible confound in the other cities' data, "
            "but is less directly tied to the argument's specific analogical "
            "assumption than (B), which asks about the Millbrook "
            "intersections themselves.\n\n"
            "Only (B) most directly tests the argument's key assumption, so "
            "(B) is correct."
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
            "It is the main conclusion of the argument.",
            "It is a claim that the argument's author explicitly rejects.",
            "It is an objection to the argument's main conclusion that the author fails to adequately address.",
            "It is a premise offered in support of the argument's conclusion that the five-a-day guideline remains achievable for low-income families.",
            "It is background information irrelevant to the argument's conclusion.",
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
]
