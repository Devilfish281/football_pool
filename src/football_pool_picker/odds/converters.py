from __future__ import annotations

import math


def american_to_prob(odds: int | float) -> float:
    """Convert American moneyline odds to implied probability (includes vig)."""
    o = float(odds)
    if o < 0:
        return abs(o) / (abs(o) + 100.0)
    return 100.0 / (o + 100.0)


def safe_american_to_prob(odds: int | float | None) -> float | None:
    if odds is None:
        return None
    try:
        return american_to_prob(odds)
    except Exception:
        return None
