"""
cleaning.py
-----------
Data cleaning and merging pipeline for Olympic dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from data_loader import load_raw_data, validate_schema

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def clean_athletes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the athlete_events DataFrame.

    Steps:
    - Impute Age, Height, Weight with sport-level medians
    - Standardize Medal column (NaN → 'No Medal')
    - Drop full duplicates
    - Encode Sex as binary flag
    """
    df = df.copy()

    # Drop duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    print(f"  Dropped {before - len(df):,} duplicate rows")

    # Impute numeric columns with sport-level medians
    for col in ["Age", "Height", "Weight"]:
        sport_median = df.groupby("Sport")[col].transform("median")
        df[col] = df[col].fillna(sport_median).fillna(df[col].median())

    # Fill medals
    df["Medal"] = df["Medal"].fillna("No Medal")

    # Binary flag
    df["IsFemale"] = (df["Sex"] == "F").astype(int)

    # Medal binary
    df["HasMedal"] = (df["Medal"] != "No Medal").astype(int)

    print(f"  Remaining nulls:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    return df


def merge_regions(athletes: pd.DataFrame, regions: pd.DataFrame) -> pd.DataFrame:
    """Merge NOC region mapping into athlete data."""
    df = athletes.merge(regions[["NOC", "region", "notes"]], on="NOC", how="left")
    df.rename(columns={"region": "Country"}, inplace=True)
    df["Country"] = df["Country"].fillna(df["Team"])
    print(f"✅ Merged regions — {df['Country'].nunique()} unique countries")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature engineering:
    - BMI from Height / Weight
    - AgeGroup bins
    - Decade from Year
    - IsHost flag placeholder
    """
    df = df.copy()

    # BMI
    df["BMI"] = (df["Weight"] / ((df["Height"] / 100) ** 2)).round(2)

    # Age groups
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 18, 25, 30, 35, 100],
        labels=["<18", "18–25", "26–30", "31–35", "35+"]
    )

    # Decade
    df["Decade"] = (df["Year"] // 10 * 10).astype(str) + "s"

    # Medal rank
    medal_rank = {"Gold": 3, "Silver": 2, "Bronze": 1, "No Medal": 0}
    df["MedalRank"] = df["Medal"].map(medal_rank)

    print("✅ Feature engineering complete")
    return df


def save_processed(df: pd.DataFrame) -> None:
    """Save cleaned DataFrame to data/processed/."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / "olympics_clean.csv"
    df.to_csv(out, index=False)
    print(f"✅ Saved processed data → {out}")


if __name__ == "__main__":
    print("🔄 Starting data cleaning pipeline...")
    athletes, regions = load_raw_data()
    validate_schema(athletes)
    athletes = clean_athletes(athletes)
    df = merge_regions(athletes, regions)
    df = engineer_features(df)
    save_processed(df)
    print("\n🏁 Pipeline complete!")
    print(df.info())
