from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd
from config import load_config
from ingestion.csv_loader import load_odds_csv
from logging_utils import get_logger
from odds.consensus import consensus
from odds.converters import safe_american_to_prob
from odds.devig import proportional_devig
from ranking.ranker import assign_confidence_ranks

LOGGER = get_logger(__name__)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Football Pool Picker")
        self.geometry("900x600")
        self.cfg = load_config()
        self.df: pd.DataFrame | None = None
        self.result: pd.DataFrame | None = None
        self._build_ui()

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill="x", padx=8, pady=8)
        tk.Button(top, text="Import CSV", command=self.on_import).pack(side="left")
        tk.Button(top, text="Compute Ranks", command=self.on_compute).pack(
            side="left", padx=8
        )
        tk.Button(top, text="Export CSV", command=self.on_export).pack(side="left")
        self.status = tk.StringVar(value="Ready.")
        tk.Label(self, textvariable=self.status, anchor="w").pack(
            fill="x", padx=8, pady=4
        )
        self.text = tk.Text(self, wrap="none")
        self.text.pack(expand=True, fill="both")

    def on_import(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.df = load_odds_csv(path)
            self.status.set(f"Loaded {len(self.df)} rows.")
            self._show(self.df.head(20))
        except Exception as e:
            LOGGER.exception("Import failed")
            messagebox.showerror("Import Error", str(e))

    def on_compute(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Please import a CSV first.")
            return
        df = self.df.copy()
        # Example: look for columns ending with "__norm" as moneylines from various books.
        ml_cols = [c for c in df.columns if c.endswith("__norm")]
        if not ml_cols:
            messagebox.showwarning(
                "No Moneylines", "No normalized moneyline columns found."
            )
            return
        # Convert each ML column to implied probabilities.
        prob_cols = []
        for c in ml_cols:
            pc = f"{c}__p"
            df[pc] = df[c].map(safe_american_to_prob)
            prob_cols.append(pc)
        # Consensus per row.
        df["consensus_prob"] = df[prob_cols].apply(
            lambda r: consensus(list(r.values), self.cfg.consensus_method), axis=1
        )
        # Optional de-vig (row-wise scale of the two outcomes would be per-game; here we scale to max=1 fallback).
        # For framework: scale probabilities into [0,1] by dividing by max if >1.
        df["consensus_prob"] = df["consensus_prob"].clip(lower=0.0, upper=1.0)
        # Assign ranks (descending).
        ranked = assign_confidence_ranks(df, prob_col="consensus_prob")
        self.result = ranked
        self.status.set("Ranks computed.")
        self._show(ranked[["consensus_prob", "confidence_rank"]].head(25))

    def on_export(self):
        if self.result is None:
            messagebox.showwarning("Nothing to Export", "Compute ranks first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        try:
            self.result.to_csv(path, index=False)
            self.status.set(f"Exported to {path}")
        except Exception as e:
            LOGGER.exception("Export failed")
            messagebox.showerror("Export Error", str(e))

    def _show(self, df: pd.DataFrame):
        self.text.delete("1.0", "end")
        self.text.insert("end", df.to_string(index=False))


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
