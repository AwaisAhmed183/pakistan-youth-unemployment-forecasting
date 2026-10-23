# Forecasting Youth Unemployment in Pakistan — Research Report

**Author:** Awais Ahmed Shah, BS Data Science (Final Year)
**Institution:** Department of Computer Science & Information Technology (CSIT),
University of Engineering and Technology (UET) Peshawar, Pakistan
**Status:** Final-year research, in progress · Non-commercial
**Code and data:** notebooks `01`–`03` in this repository; every number below is taken
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
5. **No provincial, education or seasonal breakdown yet.** The World Bank annual
   national series cannot answer where (which province) or for whom (which education
   level) unemployment is worst. That requires PBS LFS tables — the planned next stage.
6. **Single-country, single-series design.** No causal claims are made anywhere in
   this project; correlations in §5.1 are descriptive only.

## 7. Next steps

- Add verified PBS LFS tables (province, gender, education breakdowns) as a panel
  dataset and repeat the comparison at provincial level.
- Extend the feature set with education enrolment and sector indicators where public
  series exist.
- Publish a simple open dashboard for the cleaned dataset and forecasts.

## 8. References

- World Bank Open Data — Pakistan indicators (API), retrieved Oct 2026:
  https://api.worldbank.org/v2/country/PAK/indicator/SL.UEM.1524.ZS and companion
  indicators SL.UEM.1524.MA.ZS, SL.UEM.1524.FE.ZS, SL.UEM.TOTL.ZS, SL.TLF.CACT.ZS,
  NY.GDP.PCAP.CD — https://data.worldbank.org/
- Pakistan Bureau of Statistics — Labour Force Survey 2024-25:
  https://www.pbs.gov.pk/
- Author's prior internship project (method background):
  https://github.com/AwaisAhmed183/CodeAlpha_Unemployment_Analysis
