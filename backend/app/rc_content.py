"""Hand-authored Reading Comprehension passages and questions, following the
same process as app/mock_questions.py: original content, independently
verified by a fresh subagent (no memory of the marked answer) before being
kept. See the lsat-methodology skill's RC section for the named method per
question type.

Starting scope (v0.2, small on purpose): 2 passages (law, natural_science),
5 questions each. More content_areas/passages can be added the same way
later.
"""

PASSAGES = [
    {
        "id": "law_product_liability",
        "content_area": "law",
        "title": "The Evolution of Product Liability Doctrine",
        "passage_text": (
            "For much of the nineteenth century, American courts applied the "
            "doctrine of caveat emptor—\"let the buyer beware\"—to "
            "disputes between manufacturers and injured consumers. Under this "
            "doctrine, a buyer who purchased a defective product generally "
            "could not recover damages from the manufacturer unless the two "
            "parties were in \"privity of contract,\" meaning they had dealt "
            "with each other directly. Because most consumers purchased goods "
            "from retailers rather than manufacturers, this privity "
            "requirement effectively shielded manufacturers from liability "
            "even when their negligence caused serious injury.\n\n"
            "Courts justified this doctrine partly on the ground that it "
            "preserved incentives for economic activity: manufacturers, the "
            "reasoning went, should not be discouraged from producing goods "
            "by the prospect of open-ended liability to parties with whom "
            "they had no direct relationship. Critics, however, argued that "
            "caveat emptor placed the cost of manufacturing defects on the "
            "party least able to prevent them. Consumers ordinarily lacked "
            "the technical expertise to detect defects in complex "
            "manufactured goods, while manufacturers possessed both the "
            "expertise and the ability to test products before distributing "
            "them.\n\n"
            "The privity requirement began to erode in the early twentieth "
            "century. In the landmark 1916 case MacPherson v. Buick Motor "
            "Co., a New York court held that a manufacturer could be held "
            "liable for negligence even absent privity, provided the product "
            "was reasonably certain to cause injury if negligently made and "
            "the manufacturer knew the product would be used by persons "
            "other than the original buyer. This ruling did not abolish the "
            "privity requirement outright, but it substantially narrowed its "
            "practical effect, since virtually any manufactured good could "
            "be characterized as reasonably certain to cause harm if "
            "defectively made.\n\n"
            "By the mid-twentieth century, courts had moved further still, "
            "adopting the doctrine of strict products liability. Under this "
            "doctrine, a manufacturer could be held liable for injuries "
            "caused by a defective product regardless of whether the "
            "manufacturer had exercised reasonable care in producing it. A "
            "plaintiff needed only to show that the product was defective "
            "when it left the manufacturer's control and that the defect "
            "caused the injury; the manufacturer's negligence, or lack "
            "thereof, became largely irrelevant to liability.\n\n"
            "Strict liability's proponents argue that manufacturers, rather "
            "than injured consumers, are better positioned to bear and "
            "distribute the costs of product-related injuries, since "
            "manufacturers can spread those costs across all purchasers of a "
            "product line through pricing, while an individual injured "
            "consumer typically cannot spread the cost of a single injury at "
            "all. Critics of strict liability counter that it may raise "
            "production costs and consumer prices industry-wide, and that it "
            "can hold manufacturers responsible for injuries that reasonable "
            "care could not have prevented. Despite these objections, strict "
            "products liability remains the dominant approach in American "
            "courts today, though a minority of jurisdictions have "
            "reintroduced limited negligence-based defenses in recent "
            "decades."
        ),
    },
    {
        "id": "science_dinosaur_metabolism",
        "content_area": "natural_science",
        "title": "Reassessing Dinosaur Metabolism",
        "passage_text": (
            "For much of the twentieth century, paleontologists generally "
            "assumed that dinosaurs were ectothermic, or \"cold-blooded,\" "
            "organisms whose body temperature depended largely on external "
            "heat sources, much like modern reptiles. This assumption rested "
            "chiefly on dinosaurs' classification within Reptilia and on the "
            "observation that their bone structure superficially resembled "
            "that of living reptiles more than that of birds or mammals, the "
            "two groups of unambiguously endothermic, or \"warm-blooded,\" "
            "vertebrates.\n\n"
            "Beginning in the 1960s, however, a number of paleontologists "
            "began to question the ectothermic model. Their skepticism was "
            "prompted partly by the discovery of dinosaur fossils in "
            "locations that, during the Mesozoic era, would have "
            "experienced cold seasonal temperatures unsuitable for animals "
            "reliant on external heat sources to remain active. It was also "
            "prompted by anatomical evidence: several dinosaur species "
            "exhibited leg structures positioned directly beneath the body, "
            "an arrangement associated with the sustained, energetically "
            "demanding locomotion typical of endothermic animals, rather "
            "than the sprawling gait typical of ectothermic reptiles.\n\n"
            "Subsequent research examined the microscopic structure of "
            "dinosaur bone tissue itself. Bones of ectothermic animals "
            "typically show growth rings similar to tree rings, reflecting "
            "alternating periods of rapid and arrested growth tied to "
            "seasonal temperature variation. Many dinosaur bones, by "
            "contrast, showed a highly vascularized tissue structure known "
            "as fibrolamellar bone, characterized by continuous, rapid "
            "growth largely uninterrupted by seasonal cycles—a pattern "
            "more typical of endothermic animals, which sustain metabolic "
            "activity and growth regardless of external temperature.\n\n"
            "These findings led some researchers to propose that dinosaurs "
            "were fully endothermic, maintaining a constant internal body "
            "temperature much as birds and mammals do. Other researchers, "
            "noting that fibrolamellar bone has since been documented in "
            "certain modern ectothermic reptiles as well, proposed an "
            "intermediate model: that dinosaurs were mesothermic, sustaining "
            "elevated metabolic rates and body temperatures above ambient "
            "levels, but without the same degree of fine-tuned internal "
            "temperature regulation found in birds and mammals. Proponents "
            "of mesothermy point out that this intermediate strategy would "
            "have allowed large dinosaurs to sustain relatively high "
            "activity levels without incurring the substantial food "
            "requirements that full endothermy demands at large body sizes, "
            "an advantage that may help explain how dinosaurs achieved the "
            "enormous body sizes attained by some species.\n\n"
            "The debate remains unresolved, complicated by the fact that "
            "dinosaurs were an extraordinarily diverse group spanning "
            "roughly 165 million years and enormous variation in body size, "
            "and it is increasingly likely that metabolic strategy varied "
            "considerably across different dinosaur lineages rather than "
            "following a single pattern. Nonetheless, the near-universal "
            "acceptance of strict ectothermy that once characterized the "
            "field has given way to a broad consensus that at least some "
            "dinosaur lineages sustained metabolic rates substantially "
            "elevated above those of typical modern reptiles."
        ),
    },
]

RC_QUESTIONS = [
    # --- law_product_liability ---
    {
        "passage_id": "law_product_liability",
        "question_type": "rc_main_point",
        "question_stem": "Which one of the following most accurately expresses the main point of the passage?",
        "choices": [
            "The doctrine of caveat emptor was replaced by strict products liability because courts recognized that manufacturers were negligent more often than previously believed.",
            "American courts have progressively shifted from a privity-based doctrine that shielded manufacturers from most liability toward a strict liability doctrine holding manufacturers liable for defects regardless of fault, a change defended on grounds of cost distribution despite continuing objections.",
            "The 1916 case MacPherson v. Buick Motor Co. abolished the privity requirement in American product liability law.",
            "Consumers today have no legal recourse against manufacturers unless they can demonstrate the manufacturer failed to exercise reasonable care.",
            "Manufacturers are better able than consumers to detect defects in their own products, which is why strict liability has become the dominant legal doctrine.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Main Point question: identify what all paragraphs "
            "collectively build toward, not a sub-point from a single "
            "paragraph.\n\n"
            "The passage traces a doctrinal arc across its full length: "
            "caveat emptor and privity (paragraphs 1-2) -> MacPherson's "
            "erosion of privity (paragraph 3) -> strict products liability "
            "(paragraph 4) -> the cost-distribution rationale and ongoing "
            "objections (paragraph 5). (B) captures this entire arc and its "
            "stated justification.\n\n"
            "(A) misstates the reason for the shift: strict liability made "
            "negligence irrelevant, it didn't newly discover negligence.\n"
            "(C) overstates MacPherson's holding - the passage says it "
            "'narrowed' privity's effect, not abolished it.\n"
            "(D) directly contradicts strict liability, which the passage "
            "says removed the fault requirement.\n"
            "(E) takes one supporting detail (paragraph 2's point about "
            "expertise) and treats it as the reason for strict liability "
            "specifically, when the passage attributes strict liability to "
            "the cost-spreading rationale in paragraph 5.\n\n"
            "Only (B) covers the full doctrinal arc, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "law_product_liability",
        "question_type": "rc_specific_detail",
        "question_stem": "According to the passage, under the doctrine of strict products liability, a plaintiff must show that",
        "choices": [
            "the manufacturer failed to exercise reasonable care in producing the product.",
            "the product was defective when it left the manufacturer's control and that the defect caused the injury.",
            "the manufacturer and the injured party were in privity of contract.",
            "the product was reasonably certain to cause injury if negligently made.",
            "the manufacturer could have foreseen the specific type of injury that occurred.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Specific Detail question: the correct answer must "
            "be explicitly stated in the passage, not inferred.\n\n"
            "The passage states directly: 'A plaintiff needed only to show "
            "that the product was defective when it left the manufacturer's "
            "control and that the defect caused the injury' - this is (B), "
            "verbatim in substance.\n\n"
            "(A) is the opposite of what's stated - the passage says "
            "negligence 'became largely irrelevant' under strict liability.\n"
            "(C) describes the old caveat emptor/privity doctrine, not "
            "strict liability, which the passage says developed specifically "
            "because privity's role had eroded.\n"
            "(D) is the MacPherson negligence-based standard from an earlier "
            "paragraph, not the strict liability standard.\n"
            "(E) is not stated anywhere in the passage's description of "
            "strict liability.\n\n"
            "Only (B) is explicitly stated as the strict liability standard, "
            "so (B) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "law_product_liability",
        "question_type": "rc_purpose_of_reference",
        "question_stem": "The passage's discussion of MacPherson v. Buick Motor Co. primarily serves to",
        "choices": [
            "provide an example of a court applying strict products liability for the first time.",
            "illustrate a transitional step between the privity-based caveat emptor doctrine and the later doctrine of strict products liability.",
            "demonstrate that consumers rarely succeeded in product liability lawsuits before the twentieth century.",
            "refute the justifications originally offered in support of the caveat emptor doctrine.",
            "show that negligence remained the sole basis for manufacturer liability throughout the twentieth century.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Purpose of a Reference question: identify why the "
            "author included this specific case, not just what it held.\n\n"
            "The passage places MacPherson between its discussion of the "
            "privity-based caveat emptor doctrine and its discussion of "
            "strict products liability, explicitly describing the case as "
            "narrowing privity's 'practical effect' without abolishing it "
            "outright - a bridge between the two doctrines. This is (B).\n\n"
            "(A) mischaracterizes the case: MacPherson is a negligence-based "
            "ruling (liability required the product be 'reasonably certain "
            "to cause injury if negligently made'), not strict liability, "
            "which the passage introduces only in the following paragraph.\n"
            "(C) is not what the case is used to show - the passage doesn't "
            "discuss litigation success rates generally.\n"
            "(D) is closer to the critics' argument mentioned earlier in the "
            "passage, not the function of the MacPherson discussion itself.\n"
            "(E) is directly contradicted by the passage's next paragraph, "
            "which describes negligence becoming 'largely irrelevant' under "
            "strict liability.\n\n"
            "Only (B) correctly identifies the case's function in the "
            "passage's structure, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "law_product_liability",
        "question_type": "rc_strengthen_weaken",
        "question_stem": "Which one of the following, if true, would most strengthen the proponents' argument (as described in the passage) in favor of strict products liability?",
        "choices": [
            "The federal government does not currently regulate the manufacturing standards for most consumer products.",
            "Consumers who are injured by defective products often face significant, unrecoverable financial losses without legal recourse.",
            "Many manufacturers carry insurance policies that cover the cost of product liability claims, with premiums calculated based on a manufacturer's total sales volume across all consumers.",
            "Some jurisdictions have reintroduced negligence-based defenses to strict liability claims.",
            "The cost of manufacturing a product typically exceeds the cost of a single consumer's medical expenses after an injury.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is an RC Strengthen/Weaken question targeting a specific "
            "argument within the passage (proponents' cost-distribution "
            "argument), not the passage's main point.\n\n"
            "The proponents' argument, per the passage: manufacturers can "
            "'spread those costs across all purchasers of a product line "
            "through pricing,' while an individual consumer 'typically "
            "cannot spread the cost of a single injury at all.' (C) directly "
            "confirms this exact mechanism - insurance premiums calculated "
            "on total sales volume is a concrete instance of costs being "
            "spread across all purchasers via pricing.\n\n"
            "(A) is irrelevant to whether costs can be spread.\n"
            "(B) supports only half of the argument (that individuals can't "
            "spread costs) without confirming the manufacturer-side "
            "spreading mechanism the argument centers on - weaker support "
            "than (C).\n"
            "(D) works against strict liability's expansion, not for the "
            "cost-distribution argument.\n"
            "(E) is a magnitude comparison, not a claim about spreadability, "
            "and doesn't bear on the argument as stated.\n\n"
            "(C) most directly and completely confirms the cited mechanism, "
            "so (C) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "law_product_liability",
        "question_type": "rc_meaning_in_context",
        "question_stem": "In the context of the passage, the phrase \"reasonably certain to cause injury if negligently made\" (used in the discussion of MacPherson v. Buick Motor Co.) most nearly means that",
        "choices": [
            "the manufacturer must have intended for the product to cause injury.",
            "injury was a foreseeable, probable consequence of manufacturing defects in that type of product, absent reasonable care.",
            "the product had already caused injuries to multiple consumers before the lawsuit was filed.",
            "the manufacturer had actual knowledge that the specific unit sold was defective.",
            "the injury was more likely to result from consumer misuse than from any defect in the product.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Meaning in Context question: the phrase's meaning "
            "must be determined from how the surrounding sentences use it, "
            "not a dictionary definition in isolation.\n\n"
            "The surrounding text frames this as the MacPherson negligence "
            "standard: liability attached when a product 'was reasonably "
            "certain to cause injury if negligently made.' In context, this "
            "describes a general, foreseeable, probability-based standard "
            "tied to negligent manufacture of that type of product - (B).\n\n"
            "(A) confuses this foreseeability standard with intent, which "
            "the passage never discusses in connection with MacPherson.\n"
            "(C) misreads it as being about actual past injuries rather than "
            "a general predictive/foreseeability standard.\n"
            "(D) is too specific - the standard concerns the product type's "
            "general risk profile, not knowledge of one specific unit.\n"
            "(E) inverts the meaning; the phrase concerns defect-caused "
            "injury, not misuse.\n\n"
            "Only (B) captures the meaning as constrained by context, so (B) "
            "is correct."
        ),
        "verified": True,
    },
    # --- science_dinosaur_metabolism ---
    {
        "passage_id": "science_dinosaur_metabolism",
        "question_type": "rc_main_point",
        "question_stem": "Which one of the following most accurately states the main point of the passage?",
        "choices": [
            "Fibrolamellar bone structure proves conclusively that all dinosaurs were fully endothermic.",
            "Scientific understanding of dinosaur metabolism has shifted from an assumption of strict ectothermy to a more nuanced view that many dinosaur lineages sustained elevated metabolic rates, though the precise nature and extent of this remains debated.",
            "Dinosaurs were classified within Reptilia primarily because of their bone structure.",
            "Mesothermy is now the scientific consensus explanation for how large dinosaurs achieved their enormous body sizes.",
            "Modern reptiles and dinosaurs share identical patterns of bone growth.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Main Point question: identify what the passage as "
            "a whole builds toward, across all its evidence.\n\n"
            "The passage moves from the original ectothermic assumption, "
            "through anatomical and bone-tissue evidence challenging it, to "
            "competing endothermy/mesothermy proposals, and closes by "
            "stating the debate 'remains unresolved' but that the field has "
            "moved to 'a broad consensus that at least some dinosaur "
            "lineages sustained metabolic rates substantially elevated' "
            "above typical modern reptiles. (B) captures this full "
            "trajectory and its qualified conclusion.\n\n"
            "(A) overstates certainty the passage explicitly denies - "
            "fibrolamellar bone is noted to also occur in some modern "
            "ectothermic reptiles, undercutting 'proves conclusively.'\n"
            "(C) is a minor supporting detail from paragraph 1, not the main "
            "point.\n"
            "(D) overstates mesothermy as established 'consensus' when the "
            "passage presents it as one proposed model among others, and "
            "doesn't call it the consensus explanation for body size.\n"
            "(E) is contradicted - the passage discusses differences in "
            "bone growth patterns, and says fibrolamellar bone appears only "
            "in 'certain' modern ectothermic reptiles, not identically.\n\n"
            "Only (B) captures the passage's full, qualified conclusion, so "
            "(B) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "science_dinosaur_metabolism",
        "question_type": "rc_specific_detail",
        "question_stem": "The passage states that skepticism about the ectothermic model of dinosaurs was prompted in part by",
        "choices": [
            "the discovery of soft tissue preserved in dinosaur fossils.",
            "the observation that dinosaur fossils have been found in locations that would have had cold seasonal temperatures during the Mesozoic era.",
            "genetic analysis comparing dinosaurs to modern birds.",
            "the discovery that dinosaurs laid eggs in a manner similar to modern reptiles.",
            "direct measurement of dinosaur body temperature using isotopic analysis.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Specific Detail question: the answer must be "
            "explicitly stated in the passage.\n\n"
            "The passage states skepticism was 'prompted partly by the "
            "discovery of dinosaur fossils in locations that, during the "
            "Mesozoic era, would have experienced cold seasonal "
            "temperatures unsuitable for animals reliant on external heat "
            "sources' - directly matching (B).\n\n"
            "(A), (C), (D), and (E) are not mentioned anywhere in the "
            "passage - none of these forms of evidence (soft tissue, "
            "genetic analysis, egg-laying behavior, isotopic temperature "
            "measurement) appear in the text.\n\n"
            "Only (B) is explicitly stated, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "science_dinosaur_metabolism",
        "question_type": "rc_inference",
        "question_stem": "It can be inferred from the passage that fibrolamellar bone structure",
        "choices": [
            "is found exclusively in dinosaur fossils and no other animal group.",
            "is not, by itself, sufficient to establish that an animal is fully endothermic.",
            "was first discovered in modern bird skeletons before being identified in dinosaur fossils.",
            "develops only in animals that reach extremely large body sizes.",
            "cannot be examined in fossilized bone tissue.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Inference question: the answer must follow by "
            "logical entailment from the passage, without going beyond it.\n\n"
            "The passage notes that fibrolamellar bone 'has since been "
            "documented in certain modern ectothermic reptiles as well,' and "
            "that this observation is precisely what led some researchers to "
            "propose the intermediate mesothermy model rather than "
            "concluding full endothermy. This entails that the bone "
            "structure alone doesn't settle full endothermy - (B).\n\n"
            "(A) is directly contradicted by the 'certain modern ectothermic "
            "reptiles' detail.\n"
            "(C) reverses an order of discovery the passage never states.\n"
            "(D) is not supported - body size is discussed only in "
            "connection with mesothermy's advantages, not as a precondition "
            "for fibrolamellar bone.\n"
            "(E) is directly contradicted - the passage describes examining "
            "fibrolamellar structure in dinosaur bone tissue, which is by "
            "definition fossilized.\n\n"
            "Only (B) is entailed by the passage, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "science_dinosaur_metabolism",
        "question_type": "rc_application",
        "question_stem": (
            "Suppose a newly discovered species of large extinct marine reptile (not a dinosaur) is found to have "
            "limb bones positioned for sustained, energetically demanding movement, but its bone tissue shows clear "
            "seasonal growth rings rather than fibrolamellar structure. Based on the passage's discussion, this "
            "combination of findings would most likely be interpreted as"
        ),
        "choices": [
            "conclusive evidence that the species was fully endothermic.",
            "evidence presenting a mixed or ambiguous picture, since the limb evidence suggests demanding locomotion typical of endothermic animals while the bone tissue evidence suggests the temperature-dependent growth pattern typical of ectothermic animals.",
            "proof that the species belongs to Reptilia rather than to a fully endothermic group.",
            "irrelevant to questions of the species' metabolism, since metabolic strategy can only be studied in dinosaurs.",
            "definitive support for the mesothermy model specifically.",
        ],
        "correct_answer": "B",
        "explanation": (
            "This is an RC Application question: apply the passage's own "
            "evidentiary framework to a new, hypothetical case not "
            "discussed in the passage.\n\n"
            "The passage uses two independent lines of evidence for "
            "metabolism: limb/locomotor structure and bone-tissue growth "
            "pattern. In the hypothetical, these two lines point in "
            "different directions - endothermic-style limbs but "
            "ectothermic-style (seasonal ring) bone tissue - which the "
            "passage's own framework would treat as a mixed picture rather "
            "than a clean answer, matching (B).\n\n"
            "(A) ignores the conflicting bone-tissue evidence.\n"
            "(C) is wrong: the passage notes dinosaurs remained classified "
            "in Reptilia even amid the metabolism debate, so reptile "
            "classification doesn't resolve metabolic status either way.\n"
            "(D) is wrong: the passage's method (examining limb structure "
            "and bone tissue) is presented generally, not as dinosaur-"
            "exclusive.\n"
            "(E) is wrong: mesothermy is associated with fibrolamellar-type "
            "evidence in the passage, which is specifically absent here "
            "(seasonal rings are the ectothermic-pattern marker instead).\n\n"
            "Only (B) correctly applies the passage's two-part framework to "
            "this new case, so (B) is correct."
        ),
        "verified": True,
    },
    {
        "passage_id": "science_dinosaur_metabolism",
        "question_type": "rc_author_attitude",
        "question_stem": "The author's attitude toward the debate over dinosaur metabolic strategy, as presented in the passage, is best described as",
        "choices": [
            "dismissive of the mesothermy model as scientifically unfounded.",
            "confident that dinosaurs were uniformly ectothermic, consistent with their classification as reptiles.",
            "presenting the debate as substantively unresolved and likely reflecting genuine variation across an evolutionarily diverse group, while noting a shift away from the original strict-ectothermy assumption.",
            "strongly advocating for full endothermy over the mesothermy model as the more scientifically accurate view.",
            "skeptical that bone tissue structure can provide any meaningful evidence about an extinct animal's metabolism.",
        ],
        "correct_answer": "C",
        "explanation": (
            "This is an RC Author's Attitude question: identify the "
            "author's stance based on evaluative language and framing, not "
            "just the passage's factual content.\n\n"
            "The author explicitly states 'the debate remains unresolved' "
            "and that metabolic strategy 'varied considerably across "
            "different dinosaur lineages rather than following a single "
            "pattern,' while also noting the field's shift away from "
            "'near-universal acceptance of strict ectothermy.' This "
            "evenhanded, evidence-summarizing framing matches (C).\n\n"
            "(A) is unsupported - mesothermy is presented with its "
            "supporting rationale, not dismissed.\n"
            "(B) is the opposite of the passage's described shift away from "
            "strict ectothermy.\n"
            "(D) is unsupported - no clear preference for full endothermy "
            "over mesothermy is expressed; both are presented evenhandedly.\n"
            "(E) is contradicted - bone tissue evidence is discussed in "
            "detail as substantively meaningful throughout.\n\n"
            "Only (C) matches the author's actual, neutral-but-informed "
            "framing, so (C) is correct."
        ),
        "verified": True,
    },
]
