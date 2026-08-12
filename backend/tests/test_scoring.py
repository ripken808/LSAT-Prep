import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from app.scoring import (
    CANONICAL_ITEM_COUNT,
    CONVERSION_TABLE,
    MIN_ITEMS_FOR_SCALING,
    PERCENTILE_ANCHORS,
    approximate_percentile,
    is_estimated,
    percentile_band,
    scaled_score,
)


# --- table integrity -------------------------------------------------------
# A lookup table like this rots silently: a typo'd row still returns a
# plausible-looking number. These tests exist so it can't.


def test_conversion_table_covers_every_scaled_point_once():
    scaled_values = [scaled for _, scaled in CONVERSION_TABLE]
    assert sorted(scaled_values) == list(range(120, 181))


def test_conversion_table_rows_descend_on_both_columns():
    raws = [raw for raw, _ in CONVERSION_TABLE]
    scaled_values = [scaled for _, scaled in CONVERSION_TABLE]
    assert raws == sorted(raws, reverse=True)
    assert scaled_values == sorted(scaled_values, reverse=True)


def test_conversion_table_bottom_row_catches_a_zero_raw_score():
    assert CONVERSION_TABLE[-1] == (0, 120)


def test_scaled_score_is_monotonic_across_the_whole_range():
    scores = [scaled_score(n, CANONICAL_ITEM_COUNT) for n in range(CANONICAL_ITEM_COUNT + 1)]
    assert scores == sorted(scores)


def test_percentile_anchors_ascend_and_span_the_whole_scale():
    scaled_points = [scaled for scaled, _ in PERCENTILE_ANCHORS]
    percentiles = [pct for _, pct in PERCENTILE_ANCHORS]
    assert scaled_points == sorted(scaled_points)
    assert percentiles == sorted(percentiles)
    assert scaled_points[0] == 120 and scaled_points[-1] == 180


# --- boundaries ------------------------------------------------------------


def test_a_perfect_score_is_180():
    assert scaled_score(CANONICAL_ITEM_COUNT, CANONICAL_ITEM_COUNT) == 180
    assert scaled_score(52, 52) == 180


def test_zero_correct_is_120():
    assert scaled_score(0, CANONICAL_ITEM_COUNT) == 120
    assert scaled_score(0, 52) == 120


def test_every_score_lands_inside_the_120_to_180_scale():
    for total in (30, 52, CANONICAL_ITEM_COUNT):
        for correct in range(total + 1):
            assert 120 <= scaled_score(correct, total) <= 180


# --- the reduced-length case, which is the whole point of this version -----


def test_the_same_raw_count_scales_differently_on_a_shorter_test():
    """31/52 is 60% and 31/76 is 41% — they must not produce the same score.

    Reading a reduced test's raw score straight off a 76-item table is the
    specific bug this normalization exists to prevent.
    """
    on_reduced = scaled_score(31, 52)
    on_blueprint = scaled_score(31, CANONICAL_ITEM_COUNT)
    assert on_reduced > on_blueprint
    assert on_reduced - on_blueprint >= 5


def test_equal_percentages_scale_alike_regardless_of_test_length():
    # 50% either way; rounding to an equivalent raw score may differ by a
    # point, so allow a one-point spread rather than demanding equality.
    assert abs(scaled_score(26, 52) - scaled_score(38, CANONICAL_ITEM_COUNT)) <= 1


def test_is_estimated_is_true_for_reduced_and_false_at_blueprint_length():
    assert is_estimated(52) is True
    assert is_estimated(CANONICAL_ITEM_COUNT) is False


# --- guards ----------------------------------------------------------------


def test_a_test_too_short_to_scale_returns_none():
    assert scaled_score(5, MIN_ITEMS_FOR_SCALING - 1) is None
    assert scaled_score(2, 3) is None


def test_the_minimum_scalable_length_does_scale():
    assert scaled_score(15, MIN_ITEMS_FOR_SCALING) is not None


@pytest.mark.parametrize(
    "correct,total",
    [(-1, 52), (5, -1), (53, 52)],
    ids=["negative correct", "negative total", "more correct than asked"],
)
def test_impossible_scores_are_rejected(correct, total):
    with pytest.raises(ValueError):
        scaled_score(correct, total)


# --- percentile ------------------------------------------------------------


def test_percentile_band_is_returned_for_every_point_on_the_scale():
    for scaled in range(120, 181):
        assert percentile_band(scaled)


def test_percentile_rises_monotonically_with_the_score():
    percentiles = [approximate_percentile(s) for s in range(120, 181)]
    assert percentiles == sorted(percentiles)


def test_percentile_is_interpolated_between_anchors_not_floored():
    """A 154 sits four fifths of the way from the 150 anchor to the 155 anchor.

    Flooring to the anchor below would report ~45th; the real answer is ~62nd.
    The curve is steepest here, so this is where flooring does the most damage.
    """
    assert 60 <= approximate_percentile(154) <= 64
    assert approximate_percentile(154) > approximate_percentile(150)


def test_ordinal_suffixes_read_correctly():
    assert percentile_band(150).endswith("45th percentile")
    assert "~2nd percentile" == percentile_band(130)
    assert "~13th percentile" == percentile_band(140)


def test_the_ends_of_the_scale_are_described_rather_than_given_a_number():
    assert percentile_band(120) == "below the 1st percentile"
    # There is no 100th percentile; rounding 99.9 must not invent one.
    assert percentile_band(180) == "99th percentile or above"
    assert "100th" not in " ".join(percentile_band(s) for s in range(120, 181))


def test_percentile_band_rejects_a_score_off_the_scale():
    with pytest.raises(ValueError):
        percentile_band(119)
    with pytest.raises(ValueError):
        percentile_band(181)
