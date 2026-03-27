"""Input/output helpers for IPO candidate analysis."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_company_data(path: str | Path) -> pd.DataFrame:
    """Load company data from CSV."""
    return pd.read_csv(path)


def save_scored_output(df: pd.DataFrame, path: str | Path) -> None:
    """Save scored output to CSV."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
