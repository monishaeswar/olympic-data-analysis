# 🏅 Olympic Data Analysis — 120 Years of the Games

> A comprehensive data science project analyzing 120 years of Olympic history to uncover trends in athlete performance, gender participation, and global medal distribution.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

This project performs an end-to-end analysis of the [120 Years of Olympic History dataset](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) from Kaggle. It covers:

- 🌍 **Medal distribution** across nations and continents
- 👩‍🦰 **Gender participation trends** from 1896 to 2016
- 🏃 **Athlete performance metrics** — age, height, weight by sport
- 🥇 **Top-performing nations** with interactive dashboards
- 📈 **Historical medal trends** over time

---

## 🗂️ Project Structure

```
olympic-data-analysis/
│
├── data/                        # Raw and processed datasets
│   ├── raw/                     # Original Kaggle CSVs (gitignored)
│   │   ├── athlete_events.csv
│   │   └── noc_regions.csv
│   └── processed/               # Cleaned & merged data
│       └── olympics_clean.csv
│
├── notebooks/                   # Jupyter notebooks (EDA → Analysis → Viz)
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_medal_analysis.ipynb
│   ├── 04_gender_participation.ipynb
│   └── 05_interactive_dashboard.ipynb
│
├── src/                         # Reusable Python modules
│   ├── __init__.py
│   ├── data_loader.py           # Load & validate raw data
│   ├── cleaning.py              # Data cleaning pipeline
│   ├── features.py              # Feature engineering
│   ├── analysis.py              # Core analysis functions
│   └── visualizations.py       # Plotting & dashboard functions
│
├── outputs/
│   ├── figures/                 # Saved charts (PNG, HTML)
│   └── reports/                 # Summary reports
│
├── tests/                       # Unit tests
│   ├── test_cleaning.py
│   └── test_analysis.py
│
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
│
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/olympic-data-analysis.git
cd olympic-data-analysis
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Dataset

Download from Kaggle: [120 Years of Olympic History](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

Place the files inside `data/raw/`:
```
data/raw/athlete_events.csv
data/raw/noc_regions.csv
```

### 5. Run the Pipeline

```bash
# Clean and process data
python src/cleaning.py

# Run full analysis
python src/analysis.py

# Launch interactive dashboard
python src/visualizations.py
```

---

## 📊 Key Insights

| Insight | Detail |
|--------|--------|
| 🇺🇸 Most medals overall | United States leads with 5,000+ medals |
| 📈 Gender parity growth | Female athletes grew from ~2% (1900) to ~45% (2016) |
| 🏊 Best age for medals | Swimming: 18–24 yrs; Shooting: 30–45 yrs |
| 🌍 Emerging nations | China, South Korea surged post-1980 |
| ⚡ Peak performance | Most gold medalists are aged 22–26 |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `pandas` | Data manipulation |
| `numpy` | Numerical operations |
| `matplotlib` / `seaborn` | Static visualizations |
| `plotly` | Interactive charts & dashboards |
| `jupyter` | Exploratory analysis |
| `pytest` | Unit testing |

---

## 📁 Dataset Source

- **Kaggle**: [120 Years of Olympic History — Athletes and Results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
- **Rows**: ~271,000 athlete-event records
- **Columns**: Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event, Medal

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
