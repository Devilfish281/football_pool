from __future__ import annotations

from typing import Sequence


def proportional_devig(probabilities: Sequence[float]) -> list[float]:
    """Scale probabilities so they sum to 1.0 (proportional method)."""
    clean = [p for p in probabilities if p is not None]
    total = sum(clean)
    if total <= 0:
        return [0.0 for _ in probabilities]
    scale = 1.0 / total
    return [p * scale if p is not None else 0.0 for p in probabilities]
