# team_map.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Mapping, Optional


def _norm(token: str) -> str:
    """Uppercase and remove non-alphanumerics for matching."""
    return re.sub(r"[^A-Z0-9]", "", token.upper())


@dataclass(frozen=True)
class LeagueTeamName:
    """Canonical NFL team-name resolver from abbreviations or aliases."""

    _canonical: Mapping[str, str]

    @staticmethod
    def build() -> "LeagueTeamName":
        M: Dict[str, str] = {}

        def add(keys, full):
            for k in keys:
                M[_norm(k)] = full

        # --- NFC West ---
        add(["ARZ", "ARI", "AZ", "Cardinals"], "Arizona Cardinals")
        add(["LAR", "LA", "Rams"], "Los Angeles Rams")
        add(["SEA", "Seahawks"], "Seattle Seahawks")
        add(["SF", "49ERS", "SF49ERS", "NINERS"], "San Francisco 49ers")

        # --- NFC South ---
        add(["ATL", "Falcons"], "Atlanta Falcons")
        add(["CAR", "Panthers"], "Carolina Panthers")
        add(["NO", "NOR", "Saints"], "New Orleans Saints")
        add(["TB", "TBB", "Buccaneers", "Bucs"], "Tampa Bay Buccaneers")

        # --- NFC North ---
        add(["CHI", "Bears"], "Chicago Bears")
        add(["DET", "Lions"], "Detroit Lions")
        add(["GB", "Packers"], "Green Bay Packers")
        add(["MIN", "Vikings"], "Minnesota Vikings")

        # --- NFC East ---
        add(["DAL", "Cowboys"], "Dallas Cowboys")
        add(["NYG", "Giants"], "New York Giants")
        add(["PHI", "Eagles"], "Philadelphia Eagles")
        add(["WAS", "WSH", "Commanders"], "Washington Commanders")

        # --- AFC West ---
        add(["KC", "KAN", "Chiefs"], "Kansas City Chiefs")
        add(["LAC", "Chargers"], "Los Angeles Chargers")
        add(["LV", "Raiders"], "Las Vegas Raiders")
        add(["DEN", "Broncos"], "Denver Broncos")

        # --- AFC South ---
        add(["HST", "HOU", "Texans"], "Houston Texans")
        add(["IND", "Colts"], "Indianapolis Colts")
        add(["JAX", "Jaguars"], "Jacksonville Jaguars")
        add(["TEN", "Titans"], "Tennessee Titans")

        # --- AFC North ---
        add(["BLT", "BAL", "Ravens"], "Baltimore Ravens")
        add(["CIN", "Bengals"], "Cincinnati Bengals")
        add(["CLV", "CLE", "Browns"], "Cleveland Browns")
        add(["PIT", "Steelers"], "Pittsburgh Steelers")

        # --- AFC East ---
        add(["BUF", "Bills"], "Buffalo Bills")
        add(["MIA", "Dolphins"], "Miami Dolphins")
        add(["NE", "NWE", "Patriots"], "New England Patriots")
        add(["NYJ", "Jets"], "New York Jets")

        return LeagueTeamName(M)

    def to_full_name(self, token: str) -> Optional[str]:
        """Return canonical full team name or None if unknown."""
        if not token:
            return None
        t = _norm(token)
        # Special-case “ERS” fragments someone might pass like '49ers' → handled above
        return self._canonical.get(t)


resolver = LeagueTeamName.build()
full = resolver.to_full_name("WSH")  # -> "Washington Commanders"
full = resolver.to_full_name("LAC")  # -> "Los Angeles Chargers"
full = resolver.to_full_name("49ers")  # -> "San Francisco 49ers"
