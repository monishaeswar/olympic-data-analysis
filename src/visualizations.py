"""
visualizations.py
-----------------
Interactive Plotly dashboards and static matplotlib/seaborn charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from analysis import (
    medal_tally, medals_over_time, gender_participation_over_time,
    top_sports_by_medals, age_distribution_by_sport, age_vs_medals
)

FIGURES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

GOLD = "#FFD700"
SILVER = "#C0C0C0"
BRONZE = "#CD7F32"
PALETTE = [GOLD, SILVER, BRONZE, "#1f77b4", "#ff7f0e"]


# ─── Plotly Interactive Charts ─────────────────────────────────────────────────

def plot_medal_tally(df: pd.DataFrame, top_n: int = 20, save: bool = True):
    """Horizontal bar chart of top medal-winning nations."""
    tally = medal_tally(df, top_n=top_n)
    fig = px.bar(
        tally,
        y="Country", x=["Gold", "Silver", "Bronze"],
        orientation="h",
        title=f"🏅 Top {top_n} Nations by Total Medals (All-Time)",
        color_discrete_map={"Gold": GOLD, "Silver": SILVER, "Bronze": BRONZE},
        labels={"value": "Medals", "variable": "Type"},
        height=600,
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, legend_title="Medal")
    if save:
        fig.write_html(FIGURES_DIR / "medal_tally.html")
        print("✅ Saved medal_tally.html")
    return fig


def plot_medals_over_time(df: pd.DataFrame, country: str = "USA", save: bool = True):
    """Line chart of medal counts over Olympic years."""
    time_df = medals_over_time(df, country=country)
    fig = px.line(
        time_df.melt(id_vars="Year", var_name="Medal", value_name="Count"),
        x="Year", y="Count", color="Medal",
        title=f"📈 {country} Medal Trend Over Time",
        color_discrete_map={"Gold": GOLD, "Silver": SILVER, "Bronze": BRONZE},
        markers=True,
    )
    if save:
        fig.write_html(FIGURES_DIR / f"medals_over_time_{country.replace(' ', '_')}.html")
    return fig


def plot_gender_participation(df: pd.DataFrame, save: bool = True):
    """Area chart showing female athlete % over time."""
    g = gender_participation_over_time(df)
    fig = px.area(
        g, x="Year", y="Percentage",
        title="👩 Female Athlete Participation Over Time (%)",
        labels={"Percentage": "% Female Athletes"},
        color_discrete_sequence=["#e91e8c"],
    )
    fig.add_hline(y=50, line_dash="dash", line_color="gray",
                  annotation_text="50% parity line")
    if save:
        fig.write_html(FIGURES_DIR / "gender_participation.html")
    return fig


def plot_age_distribution(df: pd.DataFrame, save: bool = True):
    """Box plot of age distribution across top sports."""
    top_sports = df["Sport"].value_counts().head(12).index.tolist()
    sub = df[df["Sport"].isin(top_sports)]
    fig = px.box(
        sub, x="Sport", y="Age", color="Medal",
        title="🏃 Age Distribution by Sport & Medal",
        color_discrete_map={"Gold": GOLD, "Silver": SILVER,
                             "Bronze": BRONZE, "No Medal": "#aaaaaa"},
        height=500,
    )
    fig.update_xaxes(tickangle=45)
    if save:
        fig.write_html(FIGURES_DIR / "age_distribution.html")
    return fig


def plot_world_medal_map(df: pd.DataFrame, save: bool = True):
    """Choropleth world map of total medals by country."""
    tally = medal_tally(df, top_n=200)
    fig = px.choropleth(
        tally, locations="Country", locationmode="country names",
        color="Total", hover_name="Country",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title="🌍 Total Olympic Medals by Country (All-Time)",
    )
    if save:
        fig.write_html(FIGURES_DIR / "world_medal_map.html")
    return fig


def plot_top_sports(df: pd.DataFrame, save: bool = True):
    """Pie chart of medals by sport."""
    sports = top_sports_by_medals(df, top_n=12)
    fig = px.pie(
        sports, names="Sport", values="MedalCount",
        title="🏆 Medal Distribution Across Top Sports",
        hole=0.35,
    )
    if save:
        fig.write_html(FIGURES_DIR / "top_sports.html")
    return fig


def build_full_dashboard(df: pd.DataFrame, save: bool = True):
    """
    Combine 4 charts into a single interactive HTML dashboard.
    """
    tally = medal_tally(df, top_n=15)
    gender = gender_participation_over_time(df)
    sports = top_sports_by_medals(df, top_n=8)
    time_df = medals_over_time(df)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Top 15 Nations by Total Medals",
            "Female Athlete Participation (%)",
            "Total Medals Over Time",
            "Top 8 Sports by Medals",
        ),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "pie"}]],
    )

    # 1 - Medal tally
    for medal, color in [("Gold", GOLD), ("Silver", SILVER), ("Bronze", BRONZE)]:
        fig.add_trace(go.Bar(
            y=tally["Country"], x=tally[medal],
            name=medal, orientation="h", marker_color=color,
            showlegend=True,
        ), row=1, col=1)

    # 2 - Gender participation
    fig.add_trace(go.Scatter(
        x=gender["Year"], y=gender["Percentage"],
        fill="tozeroy", line_color="#e91e8c",
        name="Female %", showlegend=False,
    ), row=1, col=2)

    # 3 - Medals over time
    for medal, color in [("Gold", GOLD), ("Silver", SILVER), ("Bronze", BRONZE)]:
        fig.add_trace(go.Scatter(
            x=time_df["Year"], y=time_df[medal],
            name=medal, line=dict(color=color),
            showlegend=False,
        ), row=2, col=1)

    # 4 - Top sports pie
    fig.add_trace(go.Pie(
        labels=sports["Sport"], values=sports["MedalCount"],
        name="Sports", hole=0.3, showlegend=False,
    ), row=2, col=2)

    fig.update_layout(
        title_text="🏅 Olympic Data Analysis — Interactive Dashboard",
        height=800,
        barmode="stack",
        template="plotly_dark",
    )

    if save:
        out = FIGURES_DIR / "dashboard.html"
        fig.write_html(str(out))
        print(f"✅ Dashboard saved → {out}")

    return fig


# ─── Static Matplotlib Charts ──────────────────────────────────────────────────

def plot_correlation_heatmap(df: pd.DataFrame, save: bool = True):
    """Correlation heatmap of numeric athlete attributes."""
    numeric_cols = ["Age", "Height", "Weight", "BMI", "MedalRank"]
    cols = [c for c in numeric_cols if c in df.columns]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                square=True, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Correlation: Athlete Attributes vs Medal Rank")
    plt.tight_layout()
    if save:
        path = FIGURES_DIR / "correlation_heatmap.png"
        plt.savefig(path, dpi=150, bbox_inches="tight")
        print(f"✅ Saved {path}")
    plt.show()


if __name__ == "__main__":
    from data_loader import load_processed_data
    df = load_processed_data()
    print("Building dashboard...")
    build_full_dashboard(df)
    plot_medal_tally(df)
    plot_gender_participation(df)
    plot_world_medal_map(df)
    print("\n🎉 All visualizations saved to outputs/figures/")
