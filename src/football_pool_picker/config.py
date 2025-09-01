from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CONFIG_PATH = Path.home() / ".football_pool_picker" / "config.toml"
PACKAGE_DATA_DIR = Path(__file__).with_suffix("").parent / "data"


@dataclass
class AppConfig:
    timezone: str = "America/Los_Angeles"
    mapping_curve: str = "balanced"
    books: list[str] = field(
        default_factory=lambda: ["DraftKings", "FanDuel", "BetMGM"]
    )
    weights: dict[str, float] = field(default_factory=dict)
    devig: bool = True
    consensus_method: str = "mean"
    team_aliases_file: Path = PACKAGE_DATA_DIR / "team_aliases.toml"


def load_config(path: Path | None = None) -> AppConfig:
    cfg_path = path or DEFAULT_CONFIG_PATH
    if cfg_path.exists():
        with cfg_path.open("rb") as f:
            data = tomllib.load(f)
        tool = data.get("tool", {}).get("football_pool_picker", {})
        return AppConfig(
            timezone=tool.get("timezone", "America/Los_Angeles"),
            mapping_curve=tool.get("mapping_curve", "balanced"),
            books=tool.get("books", ["DraftKings", "FanDuel", "BetMGM"]),
            weights=tool.get("weights", {}),
            devig=tool.get("devig", True),
            consensus_method=tool.get("consensus_method", "mean"),
            team_aliases_file=Path(
                tool.get(
                    "team_aliases_file", str(PACKAGE_DATA_DIR / "team_aliases.toml")
                )
            ),
        )
    return AppConfig()
