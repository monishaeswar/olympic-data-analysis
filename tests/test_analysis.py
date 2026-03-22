"""
test_analysis.py
Unit tests for the analysis functions.
"""

import pandas as pd
import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from analysis import medal_tally, gender_participation_over_time, age_vs_medals


@pytest.fixture
def mock_df():
    return pd.DataFrame({
        "ID": range(10),
        "Sex": ["F", "M", "F", "M", "F", "M", "F", "M", "F", "M"],
        "Age": [22, 25, 20, 28, 24, 30, 23, 27, 21, 26],
        "Sport": ["Swimming"] * 10,
        "Year": [2000, 2000, 2004, 2004, 2008, 2008, 2012, 2012, 2016, 2016],
        "Country": ["USA", "China", "USA", "Russia", "UK", "USA", "China", "USA", "UK", "France"],
        "Medal": ["Gold", "Silver", "Bronze", "Gold", "No Medal", "Gold",
                  "Silver", "No Medal", "Bronze", "Gold"],
        "HasMedal": [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    })


def test_medal_tally_columns(mock_df):
    tally = medal_tally(mock_df, top_n=5)
    assert set(["Country", "Gold", "Silver", "Bronze", "Total"]).issubset(tally.columns)


def test_medal_tally_sorted(mock_df):
    tally = medal_tally(mock_df, top_n=5)
    assert tally["Total"].is_monotonic_decreasing


def test_gender_participation_percentage(mock_df):
    g = gender_participation_over_time(mock_df)
    assert (g["Percentage"] >= 0).all()
    assert (g["Percentage"] <= 100).all()


def test_age_vs_medals(mock_df):
    result = age_vs_medals(mock_df)
    assert "HasMedal" in result.columns
    assert len(result) <= 2  # 0 and 1
