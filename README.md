# 🍽️ Restaurant Analytics — Python EDA Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-green?style=flat-square&logo=pandas)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-purple?style=flat-square)](https://plotly.com)

> **Python-based EDA project** analyzing 9,500+ restaurants across 15 countries.  
> Built with Pandas, Matplotlib, Seaborn, Plotly, and Streamlit.

---

## 📁 Project Structure

```
python-dashboard/
├── app.py                  ← Streamlit interactive dashboard
├── Restaurant_EDA.ipynb    ← Jupyter EDA notebook (main portfolio piece)
├── requirements.txt        ← Python dependencies
├── run_dashboard.bat       ← One-click launcher
└── charts/                 ← Saved chart images (auto-created by notebook)
```

---

## 🚀 How to Run

### Option 1 — Double-click the launcher
```
Double-click run_dashboard.bat
```
Opens the Streamlit dashboard at **http://localhost:8501**

### Option 2 — Manual
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 3 — Jupyter Notebook
```bash
pip install jupyter
jupyter notebook Restaurant_EDA.ipynb
```

---

## 📊 What's Inside

### Streamlit Dashboard (`app.py`)
| Feature | Detail |
|---------|--------|
| Sidebar Filters | Filter by country, price range, minimum rating |
| 6 KPI Cards | Total restaurants, avg rating, votes, cuisines, delivery %, booking % |
| Executive Insights | 4 auto-computed business insight cards |
| Top 3 Revenue Cards | Identified via Revenue Index (Avg Cost × Votes) |
| 10 Plotly Charts | Interactive, hover-enabled, dark themed |
| Data Quality Table | Column-level completeness with color coding |
| Raw Data Explorer | Browse the cleaned dataset inline |

### Jupyter Notebook (`Restaurant_EDA.ipynb`)
| Section | Content |
|---------|---------|
| 1 | Import libraries & configure style |
| 2 | Load & inspect data (shape, dtypes, nulls, stats) |
| 3 | Data cleaning (type fixing, deduplication, feature engineering) |
| 4 | Univariate analysis (rating, votes, price distribution) |
| 5 | Cuisine analysis + Top 3 revenue-driving categories |
| 6 | Geographic analysis (countries, cities) |
| 7 | Rating & customer engagement (scatter, pie) |
| 8 | Pricing & service adoption + correlation heatmap |
| 9 | Business insights summary |

---

## 🏆 Key Findings

- **Top 3 Revenue Drivers**: North Indian › Chinese › Fast Food
- **Digital Gap**: Only ~25% of restaurants offer online delivery
- **Price-Quality**: Higher-priced restaurants consistently rate better
- **Market**: India dominates with 90%+ of all listings

---

## 🛠️ Tech Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Plotly` · `Streamlit`
