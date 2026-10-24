# Forecasting Youth Unemployment in Pakistan — Research Report

**Author:** Awais Ahmed Shah, BS Data Science (Final Year)
**Institution:** Department of Computer Science & Information Technology (CSIT),
University of Engineering and Technology (UET) Peshawar, Pakistan
**Status:** Final-year research, complete (Stage 1 + Stage 2) · Non-commercial
**Code and data:** notebooks `01`–`04` in this repository; every number below is taken
from the executed outputs of those notebooks or from the cited public sources.

---

## 1. Research question

Which patterns drive youth unemployment in Pakistan, and can interpretable
machine-learning and time-series models forecast youth unemployment accurately enough
to be useful to students, universities, and policymakers?

## 2. Why it matters

Pakistan's own Labour Force Survey 2024-25 (Pakistan Bureau of Statistics) puts the
overall unemployment rate at **7.1%**, with a labour force participation rate of
**46.3%** (PBS, https://www.pbs.gov.pk/). Young people carry a heavier burden than the
average worker: in the World Bank's modelled ILO series, youth unemployment (ages 15–24)
for Pakistan stood at **9.594% in 2025**, about **1.77×** the modelled total unemployment
rate for the same year (5.420%). Understanding and anticipating that gap is the first
step toward closing it.

## 3. Data

- **Main dataset:** six World Bank indicators for Pakistan, 1991–2025 (35 annual
  observations), fetched from the World Bank Open Data API on 23–24 Oct 2026:
  youth unemployment (total / male / female), total unemployment, labour force
  participation, and GDP per capita. Full codes, URLs and values are documented in
  `data/sources.md` and `data/DATA_DICTIONARY.md`. The dataset has **no missing values**.
- **National reference:** PBS Labour Force Survey 2024-25 headline figures (above).
  PBS and World Bank figures are *not* interchangeable — different instruments and
  methods — and are always labelled in this report.
- **Stage 2 panel (notebook 04):** six CSVs in `data/pbs_lfs_*.csv` transcribed
  cell-by-cell from the published PBS LFS 2024-25 report (37th round, September
  2025): unemployment by province × sex (Table 9.2, 19th ICLS; Table 9.3, 13th ICLS
  with rural/urban splits, 2020-21 vs 2024-25), youth (15-24) indicators by province
  × sex (Table 8.7), unemployment by age group (Tables 9.4–9.6), by education level
  (Tables 9.7–9.8), and youth NEET rates (Table 8.8). Every value was read twice
  (PDF text layer and a rendered copy) with full agreement; the retrieved PDF's
  SHA-256 is recorded in notebook 04.
- **Known data caveat:** the World Bank modelled series sits near 1% for youth
  unemployment in the early 1990s and steps up around the turn of the century. This
  likely reflects estimation/measurement conditions of that era as much as economics,
  so long-run averages over 1991–2025 must be interpreted with care.

## 4. Method

1. **Collection (notebook 01):** API download with a bundled-CSV fallback; raw JSON
   responses are preserved in `data/raw/`.
2. **EDA (notebook 02):** quality checks, trend, gender and youth-vs-total comparisons,
   context indicators; figures in `results/figures/`.
3. **Forecasting (notebook 03):** time-based hold-out — train on 1991–2015 (n = 25),
   test on 2016–2025 (n = 10) — with a consistent **one-step-ahead** evaluation for five
   models: Naive, Drift, ARIMA (order selected by AIC on the training window only),
   Linear Regression on lag features (lags 1–3 + previous 3-year rolling mean), and
   Random Forest on the same features. Metrics: MAE and RMSE in percentage points,
   saved to `results/model_metrics.csv`. The best test model is then rolled forward
   for an indicative 2026–2030 outlook.
4. **PBS panel (notebook 04):** transcription of published LFS 2024-25 tables into
   tidy CSVs with source columns, integrity checks (no missing rates, spot-checks
   against the printed report, youth counts adding up within the report's own
   0.2m rounding), computed gender gaps and youth-vs-all-ages ratios within the
   same framework and year, and three figures (fig7–fig9). 19th and 13th ICLS
   tables are never mixed.
5. **Dashboard (`dashboard/app.py`):** Streamlit app over the repo's own CSVs only —
   trend, model comparison, outlook, and the PBS panel — verified by executing the
   full script headlessly (zero exceptions) and by serving it and fetching the page
   (HTTP 200, no errors).

## 5. Results (all values from executed notebook outputs)

### 5.1 Exploratory findings

- Youth unemployment ranged from **0.820% (2007)** to **11.053% (2021)** in the modelled
  series; the 2021 peak coincides with the COVID-19 shock period. It eased to 9.448% in
  2022 and has edged up since: 9.423% (2023), 9.521% (2024), **9.594% (2025)**.
- **Gender:** young women's unemployment was higher than young men's in only 8 of 35
  years — but those years are 2008, 2015 and **every year from 2020 to 2025**. In 2025:
  female **10.143%** vs male **9.416%** (gap +0.73 pp). The highest female values in the
  series occur in 2020–2021 (14.129% and 14.278%).
- Youth unemployment correlates positively with both labour force participation
  (Pearson r = 0.845) and GDP per capita (r = 0.838) over the full period — a pattern
  dominated by common long-run trends, reported here as description, **not** causation.

### 5.2 Model comparison — test period 2016–2025, one-step-ahead

| Model | MAE (pp) | RMSE (pp) |
|---|---|---|
| **Drift** | **0.886** | **1.101** |
| Naive (last value) | 0.921 | 1.138 |
| ARIMA(2, 1, 0) | 1.185 | 1.424 |
| Linear Regression (lag features) | 1.742 | 2.011 |
| Random Forest (lag features) | 3.725 | 4.126 |

**The honest headline:** on 35 annual observations, the simple baselines beat the
machine-learning models. The Drift model (last value + the average yearly change of
+0.238 pp/year estimated on the training window) was most accurate; the Random Forest,
with only 22 supervised training rows, was clearly worst (MAE 3.72 pp) — a textbook
small-data overfitting result. More features or more complex models are **not** an
improvement at this sample size; additional *data* (PBS survey rounds, provincial
panels) is the promising direction, not additional model complexity.

### 5.3 Indicative outlook, 2026–2030 (Drift model, best on test)

| Year | Forecast youth unemployment (%) |
|---|---|
| 2026 | 9.832 |
| 2027 | 10.071 |
| 2028 | 10.309 |
| 2029 | 10.548 |
| 2030 | 10.786 |

This outlook simply extends the training-window drift rate and carries **no confidence
interval**. It is a "recent patterns continue" baseline — see limitations below before
quoting it anywhere.

### 5.4 PBS province panel — LFS 2024-25 (survey figures, notebook 04)
All figures in this section are **survey** figures from the published PBS LFS 2024-25
report, labelled with their ICLS framework. They are not comparable one-to-one with
the modelled World Bank series in §5.1–5.3 and are never plotted with them.

**Province and gender (19th ICLS, all ages, Table 9.2).** Unemployment is highest in
KP (9.6%), followed by Punjab (7.3%), Balochistan (5.5%) and Sindh (5.3%), against a
national 7.1%. The gender gap is widest in KP: females 18.1% vs males 7.5% (+10.6 pp);
nationally, females 10.5% vs males 6.0% (+4.5 pp).

**Youth by province (19th ICLS, ages 15-24, Table 8.7).** The survey youth rate is
**12.8%** nationally — 1.80× the survey all-ages rate (7.1%, same survey, framework
and year). By province: KP 15.4%, Punjab 12.9%, Balochistan 11.6%, Sindh 11.0%. The
highest single cell in the panel is **KP females aged 15-24 at 25.6%**. Punjab is the
only province where youth females (12.6%) sit below youth males (13.1%).

**Age and education (Tables 9.4, 9.7, 19th ICLS).** Unemployment is highest in the
15-24 age group (12.8%) and falls with age (65+: 0.8%). By education (all ages),
unemployment *rises* with schooling: 4.7% with no education, 6.2% below matric,
8.6% matric, peaking at 12.6% for intermediate, 10.9% degree, 11.7% Master/M.Phil/PhD.
At degree level, females face 24.1% vs males 7.0% (+17.1 pp); at Master/M.Phil/PhD,
females 24.0% vs males 6.5% (+17.5 pp). PBS publishes no youth-by-education
cross-tab in this report, so no youth education breakdown is claimed.

**Change since 2020-21 (13th ICLS, Tables 9.3, 9.5, 9.8).** National unemployment rose
from 6.3% to 6.9%; youth 15-24 from 11.1% to 12.5%; every province rose, Sindh most
(+1.2 pp, 3.9% → 5.1%). Urban unemployment (8.0%) exceeds rural (6.3%); the highest
cell in Table 9.3 is Balochistan urban females at 29.4%. Youth NEET improved
nationally (32.5% → 28.4%) but remains 45.4% for young women vs 13.0% for young men.

## 6. Limitations

1. **Tiny annual sample.** n = 35 points (25 train / 10 test). All results, especially
   ML model rankings, are fragile to this.
2. **One-step-ahead ≠ multi-year forecasting.** Test metrics measure next-year
   prediction using observed lags; the 2026–2030 outlook is necessarily weaker
   evidence than the test scores.
3. **Modelled data.** The World Bank/ILO series is modelled, not raw survey data, and
   its early-1990s segment behaves differently from later decades.
4. **Shocks are invisible to these models.** COVID-19 produced the series peak in 2021;
   floods, political and macroeconomic shocks can move the real rate far from any
   trend-based outlook.
5. **Panel limits.** The PBS youth-by-province panel is a 2024-25 cross-section only:
   no published youth-by-province time series exists in this report, so none is shown.
   The education gradient covers all ages (no published youth-by-education cross-tab).
   PBS rounds to one decimal, so small count discrepancies (≤ 0.2m) are the report's
   own rounding. Survey and modelled figures must still never be merged or averaged.
6. **Single-country, single-series design.** No causal claims are made anywhere in
   this project; correlations in §5.1 are descriptive only.

## 7. Next steps

- ~~Add verified PBS LFS tables (province, gender, education breakdowns) as a panel
  dataset and repeat the comparison at provincial level.~~ **Done in Stage 2**
  (notebook 04, `data/pbs_lfs_*.csv`, §5.4 above).
- ~~Publish a simple open dashboard for the cleaned dataset and forecasts.~~
  **Done in Stage 2** (`dashboard/app.py`, verified headless).
- Extend the feature set with education enrolment and sector indicators where public
  series exist (future work, not required for completion).

## 8. References

- World Bank Open Data — Pakistan indicators (API), retrieved Oct 2026:
  https://api.worldbank.org/v2/country/PAK/indicator/SL.UEM.1524.ZS and companion
  indicators SL.UEM.1524.MA.ZS, SL.UEM.1524.FE.ZS, SL.UEM.TOTL.ZS, SL.TLF.CACT.ZS,
  NY.GDP.PCAP.CD — https://data.worldbank.org/
- Pakistan Bureau of Statistics — *Labour Force Survey 2024-25*, 37th round,
  September 2025 (Government of Pakistan, Ministry of Planning, Development &
  Special Initiatives): https://www.pbs.gov.pk/wp-content/uploads/2020/07/LFS-2024-25-Annual-Report.pdf
  — Tables 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 8.7, 8.8 transcribed into
  `data/pbs_lfs_*.csv` (retrieved 25 Oct 2026; PDF SHA-256
  79950b81ce4d738d48ff64f5e192f7905b112724a71b5d3018f4ff5991a57d48).
- Author's prior internship project (method background):
  https://github.com/AwaisAhmed183/CodeAlpha_Unemployment_Analysis
