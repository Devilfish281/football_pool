from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_picks_csv(df: pd.DataFrame, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def export_picks_pdf(df: pd.DataFrame, path: str | Path) -> None:
    # Placeholder: in future use reportlab/WeasyPrint.
    # For now, write a simple text-based summary with .pdf extension.
    p = Path(path)
    lines = [
        "Football Pool Picker — Confidence Card",
        "",
        df.to_string(index=False),
    ]
    p.write_text("\n".join(lines), encoding="utf-8")
