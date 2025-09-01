from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TieBreakPrefs:
    order: tuple[str, ...] = ("home", "kickoff", "alpha")


def tie_key(row: dict, prefs: TieBreakPrefs) -> tuple:
    parts = []
    for rule in prefs.order:
        if rule == "home":
            parts.append(0 if row.get("favorite_is_home", False) else 1)
        elif rule == "kickoff":
            parts.append(row.get("kickoff_ts") or datetime.max)
        elif rule == "alpha":
            parts.append(str(row.get("favorite_team", "")))
    return tuple(parts)
