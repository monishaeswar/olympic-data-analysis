"""
data_loader.py
--------------
Load and validate raw Olympic datasets.
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def load_raw_data(
    athletes_path: str = None,
    regions_path: str = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load raw CSV files from the Kaggle dataset.

    Parameters
    ----------
    athletes_path : str, optional
        Custom path to athlete_events.csv
    regions_path : str, optional
        Custom path to noc_regions.csv

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (athletes_df, regions_df)
    """
    athletes_file = Path(athletes_path) if athletes_path else RAW_DIR / "athlete_events.csv"
    regions_file = Path(regions_path) if regions_path else RAW_DIR / "noc_regions.csv"

    if not athletes_file.exists():
        raise FileNotFoundError(
            f"Dataset not found at {athletes_file}.\n"
            "Download from: https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results\n"
            "and place CSV files in data/raw/"
        )

    athletes_df = pd.read_csv(athletes_file)
    regions_df = pd.read_csv(regions_file)

    print(f"✅ Loaded {len(athletes_df):,} athlete records")
    print(f"✅ Loaded {len(regions_df):,} NOC regions")

    return athletes_df, regions_df


def validate_schema(df: pd.DataFrame) -> None:
    """Assert that required columns are present."""
    required_cols = ["ID", "Name", "Sex", "Age", "Height", "Weight",
                     "Team", "NOC", "Games", "Year", "Season",
                     "City", "Sport", "Event", "Medal"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    print("✅ Schema validation passed")


def load_processed_data() -> pd.DataFrame:
    """Load the cleaned and processed dataset."""
    path = PROCESSED_DIR / "olympics_clean.csv"
    if not path.exists():
        raise FileNotFoundError("Processed data not found. Run cleaning.py first.")
    return pd.read_csv(path)
