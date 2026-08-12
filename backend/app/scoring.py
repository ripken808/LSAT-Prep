"""Raw score -> scaled score (120-180) conversion.

Pure functions, no I/O — the whole of v0.7's logic lives here so it can be
tested without a database or a fixture.

Two things about the tables below are worth knowing before changing them:

1. `CONVERSION_TABLE` is a REPRESENTATIVE composite curve, not a transcription
   of any published test form's table. Real LSAT conversion tables are equated
   per form, so a given raw score maps to slightly different scaled scores on
   different tests; there is no single "the" table to copy. This curve sits in
   the middle of the usual spread.

2. It is defined against a 76-item test (`CANONICAL_ITEM_COUNT`) because that is
   what a real scored LSAT is: 2 Logical Reasoning sections of 24-26 plus a
   Reading Comprehension section of 26-28. The app's "reduced" preset is 52
   questions, so `scaled_score` normalizes to a percentage FIRST and then looks
   up an equivalent raw score. Looking 31 up directly would read it as 31/76
   (41%, ~143) when it actually means 31/52 (60%, ~154).
"""

CANONICAL_ITEM_COUNT = 76

# Below this many questions a scaled score is noise, not a measurement — one
# item would swing it several points. The /test UI always submits a whole paper,
# but /api/test/grade is reachable with any answer list.
MIN_ITEMS_FOR_SCALING = 30

# (minimum raw score out of CANONICAL_ITEM_COUNT, scaled score), descending.
# Every scaled point 120-180 appears exactly once; tests/test_scoring.py pins
# that, because a table like this rots silently.
CONVERSION_TABLE: list[tuple[int, int]] = [
    (75, 180),
    (74, 179),
    (73, 178),
    (72, 177),
    (71, 176),
    (70, 175),
    (69, 174),
    (68, 173),
    (67, 172),
    (66, 171),
    (65, 170),
    (64, 169),
    (63, 168),
    (62, 167),
    (61, 166),
    (59, 165),
    (58, 164),
    (57, 163),
    (56, 162),
    (54, 161),
    (53, 160),
    (52, 159),
    (51, 158),
    (49, 157),
    (48, 156),
    (47, 155),
    (45, 154),
    (44, 153),
    (43, 152),
    (41, 151),
    (40, 150),
    (39, 149),
    (37, 148),
    (36, 147),
    (35, 146),
    (33, 145),
    (32, 144),
    (31, 143),
    (30, 142),
    (28, 141),
    (27, 140),
    (26, 139),
    (25, 138),
    (24, 137),
    (23, 136),
    (22, 135),
    (21, 134),
    (20, 133),
    (19, 132),
    (18, 131),
    (17, 130),
    (16, 129),
    (15, 128),
    (14, 127),
    (13, 126),
    (12, 125),
    (11, 124),
    (10, 123),
    (9, 122),
    (8, 121),
    (0, 120),
]

# (scaled score, approximate percentile) anchors. Approximate by nature: real
# percentiles are computed over a rolling three-year cohort and move year to
# year, so these are the shape of the distribution rather than exact figures.
#
# Values BETWEEN anchors are interpolated, not floored to the anchor below.
# Flooring looks harmless and isn't: the curve is steepest in the middle, where
# five scaled points span ~20 percentile points, so a 154 would be reported as
# the 150 anchor's ~45th when it is really ~62nd.
PERCENTILE_ANCHORS: list[tuple[int, float]] = [
    (120, 0.0),
    (125, 0.5),
    (130, 2.0),
    (135, 5.0),
    (140, 13.0),
    (145, 27.0),
    (150, 45.0),
    (155, 66.0),
    (160, 81.0),
    (165, 92.0),
    (170, 98.0),
    (175, 99.5),
    (180, 99.9),
]


def _ordinal(n: int) -> str:
    # 11/12/13 take "th" despite ending in 1/2/3.
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def approximate_percentile(scaled: int) -> float:
    """Interpolated percentile for a scaled score."""
    if not 120 <= scaled <= 180:
        raise ValueError(f"Scaled score outside the 120-180 scale: {scaled}.")

    for (low_scaled, low_pct), (high_scaled, high_pct) in zip(
        PERCENTILE_ANCHORS, PERCENTILE_ANCHORS[1:]
    ):
        if low_scaled <= scaled <= high_scaled:
            span = high_scaled - low_scaled
            return low_pct + (high_pct - low_pct) * (scaled - low_scaled) / span
    raise ValueError(f"No percentile anchor bracket for {scaled}.")


def scaled_score(correct: int, total: int) -> int | None:
    """Convert a raw score to the 120-180 scale.

    Returns None when `total` is below MIN_ITEMS_FOR_SCALING — a scaled score
    off a handful of questions would be a number without a meaning.
    """
    if correct < 0 or total < 0:
        raise ValueError(f"Scores cannot be negative: {correct} of {total}.")
    if correct > total:
        raise ValueError(f"Cannot score {correct} correct out of {total}.")
    if total < MIN_ITEMS_FOR_SCALING:
        return None

    equivalent_raw = round(correct / total * CANONICAL_ITEM_COUNT)
    for minimum_raw, scaled in CONVERSION_TABLE:
        if equivalent_raw >= minimum_raw:
            return scaled
    # Unreachable: the table's last row has a floor of 0 and raw is never
    # negative. Kept so a truncated table fails loudly rather than returning None.
    raise ValueError(f"No conversion row for equivalent raw score {equivalent_raw}.")


def percentile_band(scaled: int) -> str:
    """Human-readable approximate percentile for a scaled score."""
    percentile = approximate_percentile(scaled)
    if percentile < 1:
        return "below the 1st percentile"
    # Never round up into a "100th percentile", which does not exist — the top
    # anchor is 99.9 and rounding it would claim every test taker scored lower.
    if percentile >= 99:
        return "99th percentile or above"
    return f"~{_ordinal(round(percentile))} percentile"


def is_estimated(total: int) -> bool:
    """Whether the scaled score was extrapolated from a non-blueprint-length test.

    Flips to False on its own once the bank can fill a real 76-question paper —
    no code change needed then.
    """
    return total != CANONICAL_ITEM_COUNT
