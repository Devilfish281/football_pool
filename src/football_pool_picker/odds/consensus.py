from __future__ import annotations

from statistics import mean, median
from typing import Iterable


def trimmed_mean(values: list[float], trim: int = 1) -> float:
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return float("nan")
    if 2 * trim >= len(vals):
        return mean(vals)
    return mean(vals[trim:-trim])


def weighted_mean(
    values: list[float], weights: dict[str, float], labels: list[str]
) -> float:
    pairs = [
        (v, weights.get(lbl, 1.0)) for v, lbl in zip(values, labels) if v is not None
    ]
    if not pairs:
        return float("nan")
    total_w = sum(w for _, w in pairs)
    if total_w == 0:
        return mean(v for v, _ in pairs)
    return sum(v * w for v, w in pairs) / total_w


def consensus(
    values: list[float],
    method: str = "mean",
    *,
    weights: dict[str, float] | None = None,
    labels: list[str] | None = None,
) -> float:
    clean = [v for v in values if v is not None]
    if not clean:
        return float("nan")
    m = method.lower()
    if m == "mean":
        return mean(clean)
    if m == "median":
        return median(clean)
    if m == "trimmed":
        return trimmed_mean(clean, trim=1)
    if m == "weighted" and weights is not None and labels is not None:
        return weighted_mean(values, weights, labels)
    return mean(clean)
