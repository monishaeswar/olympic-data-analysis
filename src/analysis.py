"""
analysis.py
-----------
Core analytical functions for Olympic data.
"""

import pandas as pd
import numpy as np


# ─── Medal Analysis ────────────────────────────────────────────────────────────

def medal_tally(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Compute medal tally by country.

    Returns a DataFrame with Gold, Silver, Bronze, Total columns.
    """
    medals = df[df["Medal"] != "No Medal"].copy()
    tally = (
        medals.groupby(["Country", "Medal"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["Gold", "Silver", "Bronze"], fill_value=0)
    )
    tally["Total"] = tally.sum(axis=1)
    tally = tally.sort_values("Total", ascending=False).head(top_n)
    return tally.reset_index()


def medals_over_time(df: pd.DataFrame, country: str = None) -> pd.DataFrame:
    """
    Medal counts by year. Optionally filter by country.
    """
    medals = df[df["Medal"] != "No Medal"].copy()
    if country:
        medals = medals[medals["Country"] == country]
    return (
        medals.groupby(["Year", "Medal"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["Gold", "Silver", "Bronze"], fill_value=0)
        .reset_index()
    )


def top_sports_by_medals(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Top sports by total medals awarded."""
    return (
        df[df["Medal"] != "No Medal"]
        .groupby("Sport")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="MedalCount")
    )


# ─── Gender Analysis ───────────────────────────────────────────────────────────

def gender_participation_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage of female athletes per Olympic year.
    """
    g = df.groupby(["Year", "Sex"]).agg(Count=("ID", "nunique")).reset_index()
    total = g.groupby("Year")["Count"].transform("sum")
    g["Percentage"] = (g["Count"] / total * 100).round(2)
    return g[g["Sex"] == "F"][["Year", "Count", "Percentage"]].reset_index(drop=True)


def gender_medal_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Medal win rate by gender."""
    return (
        df.groupby("Sex")
        .agg(
            TotalAthletes=("ID", "nunique"),
            MedalWins=("HasMedal", "sum")
        )
        .assign(WinRate=lambda x: (x["MedalWins"] / x["TotalAthletes"] * 100).round(2))
        .reset_index()
    )


# ─── Athlete Performance ───────────────────────────────────────────────────────

def age_distribution_by_sport(df: pd.DataFrame, sports: list = None) -> pd.DataFrame:
    """Age stats for top sports or a specified list."""
    if sports:
        df = df[df["Sport"].isin(sports)]
    else:
        top = df["Sport"].value_counts().head(15).index
        df = df[df["Sport"].isin(top)]
    return (
        df.groupby("Sport")["Age"]
        .agg(["mean", "median", "std", "min", "max"])
        .round(1)
        .reset_index()
        .rename(columns={"mean": "AvgAge", "median": "MedianAge",
                          "std": "StdAge", "min": "MinAge", "max": "MaxAge"})
    )


def age_vs_medals(df: pd.DataFrame) -> pd.DataFrame:
    """Compare average age of medal winners vs non-winners."""
    return (
        df.groupby("HasMedal")["Age"]
        .agg(["mean", "median", "count"])
        .round(2)
        .reset_index()
        .rename(columns={"mean": "AvgAge", "median": "MedianAge", "count": "Count"})
    )


def host_country_advantage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze medal count of the host country vs its overall average.
    Maps Games → host country from a lookup dict.
    """
    host_map = {
        "1896 Summer": "Greece", "1900 Summer": "France",
        "1904 Summer": "USA", "1908 Summer": "UK",
        "1912 Summer": "Sweden", "1920 Summer": "Belgium",
        "1924 Summer": "France", "1928 Summer": "Netherlands",
        "1932 Summer": "USA", "1936 Summer": "Germany",
        "1948 Summer": "UK", "1952 Summer": "Finland",
        "1956 Summer": "Australia", "1960 Summer": "Italy",
        "1964 Summer": "Japan", "1968 Summer": "Mexico",
        "1972 Summer": "Germany", "1976 Summer": "Canada",
        "1980 Summer": "Russia", "1984 Summer": "USA",
        "1988 Summer": "South Korea", "1992 Summer": "Spain",
        "1996 Summer": "USA", "2000 Summer": "Australia",
        "2004 Summer": "Greece", "2008 Summer": "China",
        "2012 Summer": "UK", "2016 Summer": "Brazil",
    }
    df = df.copy()
    df["HostCountry"] = df["Games"].map(host_map)
    df["IsHost"] = df["Country"] == df["HostCountry"]
    return (
        df[df["Medal"] != "No Medal"]
        .groupby("IsHost")
        .size()
        .reset_index(name="Medals")
    )


if __name__ == "__main__":
    from data_loader import load_processed_data
    df = load_processed_data()

    print("\n🥇 Top 10 Medal Tallies:")
    print(medal_tally(df, top_n=10).to_string(index=False))

    print("\n👩 Gender participation (last 5 years):")
    print(gender_participation_over_time(df).tail(5).to_string(index=False))

    print("\n📊 Age vs Medal win:")
    print(age_vs_medals(df).to_string(index=False))
