"""Scoring utilities for IPO candidate analysis."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class ScoreWeights:
    growth: float = 0.25
    quality: float = 0.20
    market: float = 0.20
    readiness: float = 0.20
    risk: float = 0.15


def clamp(series: pd.Series, lower: float = 0.0, upper: float = 10.0) -> pd.Series:
    """Clamp a numeric series to the specified range."""
    return series.clip(lower=lower, upper=upper)


def build_component_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build component scores on a 0-10 scale.

    Expected input columns:
    - revenue_growth_pct
    - gross_margin_pct
    - market_size_score
    - governance_score
    - profitability_trend_score
    - capital_intensity_score
    - regulatory_risk_score
    """
    out = df.copy()

    out["growth_score"] = clamp(out["revenue_growth_pct"] / 10)
    out["quality_score"] = clamp((out["gross_margin_pct"] / 10 + out["profitability_trend_score"]) / 2)
    out["market_score"] = clamp(out["market_size_score"])
    out["readiness_score"] = clamp(out["governance_score"])
    # Higher risk inputs should reduce the final score, so we invert them.
    out["risk_score"] = clamp(10 - ((out["capital_intensity_score"] + out["regulatory_risk_score"]) / 2))

    return out


def calculate_total_score(df: pd.DataFrame, weights: ScoreWeights | None = None) -> pd.DataFrame:
    """Calculate the weighted total score."""
    weights = weights or ScoreWeights()
    scored = build_component_scores(df)

    scored["total_score"] = (
        scored["growth_score"] * weights.growth
        + scored["quality_score"] * weights.quality
        + scored["market_score"] * weights.market
        + scored["readiness_score"] * weights.readiness
        + scored["risk_score"] * weights.risk
    )

    return scored.sort_values("total_score", ascending=False).reset_index(drop=True)
