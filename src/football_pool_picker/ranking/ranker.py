from __future__ import annotations

import math

import pandas as pd
from ranking.tiebreakers import TieBreakPrefs, tie_key


def _rank_range(n: int) -> list[int]:
    return list(range(n, 0, -1))


def assign_confidence_ranks(
    games: pd.DataFrame,
    *,
    prob_col: str = "consensus_prob",
    tiebreak_prefs: TieBreakPrefs | None = None,
) -> pd.DataFrame:
    """Assign unique confidence ranks N..1 by descending probability + tie-breaks."""
    prefs = tiebreak_prefs or TieBreakPrefs()
    df = games.copy()
    if prob_col not in df.columns:
        raise KeyError(f"Missing probability column: {prob_col}")
    # Build a deterministic sort key per row.
    sort_keys = []
    for _, r in df.iterrows():
        sort_keys.append((float(r[prob_col] or 0.0), tie_key(r.to_dict(), prefs)))
    df = df.assign(__sort_key=sort_keys)
    df = df.sort_values(by="__sort_key", ascending=False).drop(columns="__sort_key")
    ranks = _rank_range(len(df))
    df["confidence_rank"] = ranks
    return df
