"""
test_cleaning.py
Unit tests for the cleaning pipeline.
"""

import pandas as pd
import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from cleaning import clean_athletes, engineer_features


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5],
        "Name": ["Alice", "Bob", "Alice", "Dan", "Eve"],
        "Sex": ["F", "M", "F", "M", "F"],
        "Age": [25.0, np.nan, 25.0, 30.0, np.nan],
        "Height": [165.0, 180.0, 165.0, np.nan, 170.0],
        "Weight": [60.0, 80.0, 60.0, 75.0, np.nan],
        "Team": ["USA", "UK", "USA", "France", "Japan"],
        "NOC": ["USA", "GBR", "USA", "FRA", "JPN"],
        "Games": ["2000 Summer"] * 5,
        "Year": [2000] * 5,
        "Season": ["Summer"] * 5,
        "City": ["Sydney"] * 5,
        "Sport": ["Swimming"] * 5,
        "Event": ["100m Freestyle"] * 5,
        "Medal": ["Gold", np.nan, "Gold", "Silver", np.nan],
    })


def test_drop_duplicates(sample_df):
    cleaned = clean_athletes(sample_df)
    assert len(cleaned) == 4  # Alice row 3 is duplicate of row 1


def test_medal_fill(sample_df):
    cleaned = clean_athletes(sample_df)
    assert "No Medal" in cleaned["Medal"].values
    assert cleaned["Medal"].isna().sum() == 0


def test_is_female_flag(sample_df):
    cleaned = clean_athletes(sample_df)
    assert set(cleaned["IsFemale"].unique()).issubset({0, 1})


def test_has_medal_flag(sample_df):
    cleaned = clean_athletes(sample_df)
    assert "HasMedal" in cleaned.columns


def test_engineer_features(sample_df):
    cleaned = clean_athletes(sample_df)
    df = engineer_features(cleaned)
    assert "BMI" in df.columns
    assert "AgeGroup" in df.columns
    assert "Decade" in df.columns
    assert "MedalRank" in df.columns


def test_bmi_positive(sample_df):
    cleaned = clean_athletes(sample_df)
    df = engineer_features(cleaned)
    assert (df["BMI"].dropna() > 0).all()
