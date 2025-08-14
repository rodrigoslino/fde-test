import pytest
from sorter import sort
import math


@pytest.mark.parametrize(
    "w, h, l, m, expected",
    [
        # bulky by volume only
        (100, 100, 100, 10, "SPECIAL"),
        # heavy only
        (10, 10, 10, 25, "SPECIAL"),
        # both bulky and heavy
        (200, 50, 50, 30, "REJECTED"),
        # neither
        (50, 40, 30, 5, "STANDARD"),
        # just below every limit
        (149.9, 149.9, 44, 19.9, "STANDARD"),
        # exactly on bulky dimension
        (150, 10, 10, 19, "SPECIAL"),
        # exactly on heavy mass
        (100, 100, 100, 20, "REJECTED"),
        # exactly both limits
        (150, 10, 10, 20, "REJECTED"),
        # exactly on volume cutoff
        (10, 10, 10, 20, "SPECIAL"),
        # just below volume cutoff
        (99.99999, 100, 100, 19, "STANDARD"),
        # just above volume cutoff
        (100.1, 100, 100, 19, "SPECIAL"),
        # just below bulky dimension cutoff
        (149.9, 10, 10, 19, "STANDARD"),
        # just above bulky dimension cutoff
        (150.1, 10, 10, 19, "SPECIAL"),
        # large mass
        (10, 10, 10, 1e6, "SPECIAL"),
        # large float values
        (1e6, 1e6, 1e6, 0.5, "SPECIAL"),
    ],
)
def test_sort_normal_cases(w, h, l, m, expected):
    assert sort(w, h, l, m) == expected


@pytest.mark.parametrize(
    "bad_value",
    [0, -1, -0.1],
)
def test_negative_or_zero_dimensions_raise(bad_value):
    with pytest.raises(ValueError):
        sort(bad_value, 10, 10, 5)
    with pytest.raises(ValueError):
        sort(10, bad_value, 10, 5)
    with pytest.raises(ValueError):
        sort(10, 10, bad_value, 5)
    with pytest.raises(ValueError):
        sort(10, 10, 10, bad_value)


@pytest.mark.parametrize(
    "w, h, l, m",
    [
        (10000, 0.001, 0.001, 10),
        (0.001, 10000, 0.001, 10),
        (0.001, 0.001, 10000, 10),
    ],
)
def test_extremely_unbalanced_dimensions(w, h, l, m):
    """One very large dimension should still mark the package as bulky."""
    assert sort(w, h, l, m) == "SPECIAL"


@pytest.mark.parametrize("bad_bool", [True, False])
def test_bool_raises_type_error(bad_bool):
    with pytest.raises(TypeError):
        sort(bad_bool, 10, 10, 5)
    with pytest.raises(TypeError):
        sort(10, bad_bool, 10, 5)
    with pytest.raises(TypeError):
        sort(10, 10, bad_bool, 5)
    with pytest.raises(TypeError):
        sort(10, 10, 10, bad_bool)


@pytest.mark.parametrize("non_numeric_value", ["a", [], None, {}, 1.0j])
def test_non_numeric_raises_type_error(non_numeric_value):
    with pytest.raises(TypeError):
        sort(non_numeric_value, 10, 10, 5)
    with pytest.raises(TypeError):
        sort(10, non_numeric_value, 10, 5)
    with pytest.raises(TypeError):
        sort(10, 10, non_numeric_value, 5)
    with pytest.raises(TypeError):
        sort(10, 10, 10, non_numeric_value)


@pytest.mark.parametrize("bad_math_value", [math.nan, math.inf, -math.inf])
def test_bad_math_value_raises_value_error(bad_math_value):
    with pytest.raises(ValueError):
        sort(bad_math_value, 10, 10, 5)
    with pytest.raises(ValueError):
        sort(10, bad_math_value, 10, 5)
    with pytest.raises(ValueError):
        sort(10, 10, bad_math_value, 5)
    with pytest.raises(ValueError):
        sort(10, 10, 10, bad_math_value)
