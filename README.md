# Forecasting Youth Unemployment in Pakistan

**Final-Year Research Project (in progress)**
Awais Ahmed Shah — BS Data Science (Final Year)
Department of Computer Science & Information Technology (CSIT)
University of Engineering and Technology (UET) Peshawar, Pakistan

## Research question
Which factors most reliably drive youth unemployment in Pakistan, and can interpretable machine-learning models forecast youth unemployment trends accurately enough to be useful to students, universities, and policymakers?

## Why this matters
Pakistan's overall unemployment rate was 7.1% in the Pakistan Bureau of Statistics (PBS) Labour Force Survey 2024-25, with young people and women facing substantially higher rates. Youth unemployment (ages 15-24, World Bank series) was 9.59% in 2025. Understanding which province, gender, education, and seasonal patterns drive these numbers is the first step to fixing them.

## Background — this project builds on real prior work
- My internship project, [CodeAlpha_Unemployment_Analysis](https://github.com/AwaisAhmed183/CodeAlpha_Unemployment_Analysis), analysed unemployment trends using Python (Pandas, NumPy, Matplotlib/Seaborn) — exploratory data analysis and visualisation on real unemployment datasets. Its stated future work was: apply machine-learning models for prediction and build an interactive dashboard. **This project is that future work, now applied to Pakistan.**
- I have also built a complete, complex software project using Google's Gemini 4 Argon model — [AURA ONE](https://github.com/AwaisAhmed183/AURA-ONE), a real-time 3D product site (React, Three.js, GSAP) built with Argon in Google AI Studio and verified end-to-end. I am applying for Google Antigravity's scientist access to use the same Argon-driven, multi-step workflow for this research.

## Data sources (all public, non-commercial research use)
- World Bank Open Data API — Pakistan labour indicators, 1991–2025 (six series: youth unemployment total/male/female, total unemployment, labour force participation, GDP per capita). Exact codes and retrieval details: `data/sources.md`
- Pakistan Bureau of Statistics — Labour Force Survey 2024-25 headline figures (overall unemployment 7.1%, participation 46.3%) (https://www.pbs.gov.pk/)
- My prior internship datasets (India unemployment CSVs) for method development and comparison

## Method
1. Clean and harmonise multi-year labour-force data into one documented, reproducible dataset (`notebooks/01`, `02`)
2. Exploratory analysis by gender and age group, youth vs total unemployment (`notebooks/02`)
3. Forecast comparison on a time-based hold-out (train 1991–2015, test 2016–2025, one-step-ahead): Naive, Drift, ARIMA, Linear Regression and Random Forest on lag features (`notebooks/03`)
4. Verify every result against the executed notebook outputs — no number appears in the report that cannot be traced to source data or a saved result file
5. Planned: add PBS province/education tables and publish findings as an open report and simple dashboard

## First results (from executed notebooks — see `report/research_report.md`)
- Youth unemployment 2025: **9.594%** (World Bank modelled ILO series), ≈ **1.77×** the total unemployment rate (5.420%).
- Series peak: **11.053% in 2021** (COVID-19 period); female youth unemployment exceeded male in every year 2020–2025 (2025: 10.143% vs 9.416%).
- Best forecasting model on the 2016–2025 test years was the simple **Drift** baseline (MAE **0.886** pp), ahead of Naive (0.921), ARIMA(2,1,0) (1.185), Linear Regression (1.742) and Random Forest (3.725) — with only 35 annual observations, simple baselines beat ML models. Full metrics: `results/model_metrics.csv`.
- Indicative Drift outlook: youth unemployment rising slowly to ≈ **10.79% by 2030** — a "recent patterns continue" baseline with wide real-world uncertainty, **not** a promise. Read the limitations in the report before quoting it.

## Repository structure
```
├── data/
│   ├── raw/            # World Bank API JSON responses + long-format CSV (exact values)
│   ├── processed/      # Wide analysis-ready CSVs (1991–2025)
│   ├── sources.md      # Where every number comes from
│   └── DATA_DICTIONARY.md
├── notebooks/
│   ├── 01_data_collection.ipynb      # World Bank API fetch (+ offline fallback)
│   ├── 02_cleaning_and_eda.ipynb     # Cleaning checks + EDA charts
│   └── 03_forecasting_models.ipynb   # Baselines, ARIMA, LR, Random Forest + outlook
├── results/
│   ├── figures/              # fig1–fig6 PNG charts from the executed notebooks
│   ├── model_metrics.csv     # MAE / RMSE per model on 2016–2025 test years
│   └── forecast_2026_2030.csv
├── report/
│   └── research_report.md    # Full research report (results, limitations, references)
├── requirements.txt
└── LICENSE
```

## How to run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook   # open notebooks/ and run 01 → 02 → 03 in order, top to bottom
```
Notebook 01 downloads fresh data from the World Bank API when online and falls back to
the bundled raw CSV when offline, so the pipeline reproduces either way. The notebooks
in this repo are committed **with their executed outputs**, and `results/` holds the
exact files those runs produced.

## Tools
Python, Pandas, NumPy, scikit-learn, statsmodels, Matplotlib, Jupyter — and Google Antigravity with Gemini 4 Argon for building the reproducible pipeline, running model experiments in parallel, and verifying outputs (application in progress).

## Status
In progress — first stage complete (World Bank dataset, EDA, forecast comparison, report).
Next stage: verified PBS LFS tables (province / gender / education) and an open dashboard.
Final-year undergraduate research, non-commercial, conducted at UET Peshawar.

## Author
Awais Ahmed Shah — Final-year BS Data Science, UET Peshawar
GitHub: https://github.com/AwaisAhmed183
