"""Screening helpers for IPO candidate analysis."""
from __future__ import annotations

import pandas as pd


def filter_candidate_universe(
    df: pd.DataFrame,
    min_growth_pct: float = 15.0,
    min_gross_margin_pct: float = 20.0,
    min_governance_score: float = 4.0,
) -> pd.DataFrame:
    """
    Apply a simple first-pass filter to the candidate universe.
    Adjust thresholds to match the sector and research style.
    """
    mask = (
        (df["revenue_growth_pct"] >= min_growth_pct)
        & (df["gross_margin_pct"] >= min_gross_margin_pct)
        & (df["governance_score"] >= min_governance_score)
    )
    return df.loc[mask].copy()
