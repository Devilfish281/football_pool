from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from dateutil import parser as dtparser
from logging_utils import anonymize_team, get_logger

LOGGER = get_logger(__name__)

UNICODE_MINUS = "\u2212"


def _normalize_moneyline_value(val) -> int | None:
    if pd.isna(val):
        return None
    s = str(val).strip()
    s = s.replace(UNICODE_MINUS, "-")
    s = re.sub(r"[^\d\-\+]", "", s)
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _parse_kickoff(val: str) -> pd.Timestamp | None:
    if pd.isna(val):
        return None
    try:
        dt = dtparser.parse(str(val))
        return (
            pd.Timestamp(dt).tz_localize(dt.tzinfo)
            if dt.tzinfo
            else pd.Timestamp(dt).tz_localize("UTC")
        )
    except Exception:
        return None


def load_odds_csv(path: str | Path) -> pd.DataFrame:
    """Load a user-provided CSV of moneylines; returns a normalized DataFrame."""
    path = Path(path)
    df = pd.read_csv(path)
    # Best-effort normalize common columns; users can remap in UI later.
    candidate_team_cols = [
        c for c in df.columns if re.search(r"team|matchup|home|away", c, re.I)
    ]
    if not candidate_team_cols:
        LOGGER.warning("No team columns detected.")
    # Normalize moneyline columns (keep originals in place as well).
    for col in df.columns:
        if re.search(r"ml|moneyline|odds", col, re.I):
            df[f"{col}__norm"] = df[col].map(_normalize_moneyline_value)
    # Kickoff parsing if present.
    ko_cols = [c for c in df.columns if re.search(r"kickoff|start|time|date", c, re.I)]
    if ko_cols:
        first = ko_cols[0]
        df["kickoff_ts"] = df[first].map(_parse_kickoff)
    # Log a tiny anonymized sample for observability.
    sample = df.head(3).copy()
    team_col = next(iter(candidate_team_cols), None)
    if team_col:
        sample[team_col] = sample[team_col].astype(str).map(anonymize_team)
    LOGGER.info("CSV loaded; rows=%s, cols=%s", len(df), len(df.columns))
    return df
