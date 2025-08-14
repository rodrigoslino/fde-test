"""
Package-sorting logic for FDE screen.

A package is:
- bulky  if volume >= 1 000 000 cm³ **or** any dimension >= 150 cm
- heavy  if mass   >= 20 kg

Stacks:
- STANDARD : neither bulky nor heavy
- SPECIAL  : bulky XOR heavy
- REJECTED : bulky AND heavy
"""

from typing import Union
import math

VOLUME_CUTOFF = 1_000_000  # cm³
BULKY_DIMENSION_CUTOFF = 150  # cm
MASS_CUTOFF = 20  # kg

Number = Union[int, float]


def _validate(name: str, value: Number) -> None:
    # Reject bool explicitly (bool is a subclass of int) and any non numeric type
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}")
    # Reject NaN and inf which would otherwise silently pass validation
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{name} cannot be NaN")
    # Reject negative values
    if value <= 0:
        raise ValueError(f"{name} must be positive (got {value!r})")


def sort(width: Number, height: Number, length: Number, mass: Number) -> str:
    """Return the stack for a package: 'STANDARD', 'SPECIAL', or 'REJECTED'."""
    # basic validation
    for label, v in (
        ("width", width),
        ("height", height),
        ("length", length),
        ("mass", mass),
    ):
        _validate(label, v)

    # compute
    volume = width * height * length
    bulky = (
        volume >= VOLUME_CUTOFF or max(width, height, length) >= BULKY_DIMENSION_CUTOFF
    )
    heavy = mass >= MASS_CUTOFF

    # classify
    if bulky and heavy:
        return "REJECTED"
    if bulky or heavy:
        return "SPECIAL"
    return "STANDARD"
