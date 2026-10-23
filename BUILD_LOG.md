# Build Log — pakistan-youth-unemployment-forecasting (staging build)

Built: 24 Oct 2026 (PKT), staging folder `~/workspace/youth-unemployment-repo/`
Author of project: Awais Ahmed Shah · Status: complete first stage, fully executed locally.
Nothing was pushed to GitHub in this build — staging only.

## Environment
- VM: Python 3.12.3. System site-packages already had pandas 2.1.4, numpy, nbformat 5.9.1;
  scikit-learn and statsmodels were missing, and the system matplotlib (3.6.3) conflicted
  with the venv's IPython 9.x (`backend2gui` import error on first execution attempt).
- Fix applied: created `.venv/` (with `--system-site-packages`) inside the staging folder and
  pip-installed into it: scikit-learn 1.9.1, statsmodels 0.15.0, nbconvert, ipykernel,
  and matplotlib upgraded to 3.11.2. Registered kernelspec `youth-venv`.
- After the fix, all three notebooks executed end-to-end with **zero cell errors**
  (verified programmatically), and notebooks were rebuilt fresh + re-executed once more
  after a wording correction in notebook 02 (see "Honesty fix" below).

## Data fetched (real, from source)
- World Bank Open Data API via `curl` and re-verified inside notebook 01:
  `https://api.worldbank.org/v2/country/PAK/indicator/<CODE>?date=1991:2025&per_page=100&format=json`
  for SL.UEM.1524.ZS, SL.UEM.1524.MA.ZS, SL.UEM.1524.FE.ZS, SL.UEM.TOTL.ZS,
  SL.TLF.CACT.ZS, NY.GDP.PCAP.CD. All six series returned complete 1991–2025 data
  (35 values each, no missing values).
- **Headline check:** youth unemployment total, Pakistan, 2025 = **9.594%** — matches the
  9.59% figure verified earlier in project research. API responses carry a World Bank
  "lastupdated" stamp of 2026-10-08.
- Raw JSON responses saved to `data/raw/`; values transcribed to
  `data/raw/worldbank_pakistan_long.csv`; wide table at
  `data/processed/pakistan_labour_indicators_1991_2025.csv`.
- PBS Labour Force Survey 2024-25 headline figures (overall unemployment 7.1%,
  participation 46.3%) were verified earlier in this project from pbs.gov.pk and are
  documented in `data/sources.md`. An attempt during this build to pull further PBS
  detail from the PBS website returned a page shell without usable table text, so **no
  additional PBS figures were added** — by design, only verified numbers enter this repo.

## Executed — real headline results
- Notebook 02 (EDA): youth unemployment range 0.820% (2007) – 11.053% (2021);
  2025 = 9.594%; female 2025 = 10.143% vs male 9.416%; youth/total ratio 2025 = 1.77×;
  correlations: youth vs participation r = 0.845, youth vs GDP per capita r = 0.838
  (descriptive only). Figures fig1–fig4 written to `results/figures/`.
- Notebook 03 (models, train 1991–2015, test 2016–2025, one-step-ahead):
  Drift MAE 0.886 / RMSE 1.101 · Naive 0.921 / 1.138 · ARIMA(2,1,0) 1.185 / 1.424 ·
  Linear Regression 1.742 / 2.011 · Random Forest 3.725 / 4.126 (pp).
  Full table: `results/model_metrics.csv`. Figures fig5–fig6 written.
- Outlook (Drift, best test model, rolled forward): 2026 = 9.832 … 2030 = 10.786
  (`results/forecast_2026_2030.csv`). It has no confidence interval and is labelled
  indicative in the notebook, report and README.

## Honesty fix made during the build
Notebook 02's draft key-findings cell originally claimed female youth unemployment was
higher "in most years". The executed output showed that is true in only 8 of 35 years
(2008, 2015, and every year 2020–2025). The text was corrected to the executed numbers
and the notebook was re-executed so the committed outputs match the committed words.

## Deliverables written
README.md (updated from the repo's existing README), report/research_report.md,
data/sources.md, data/DATA_DICTIONARY.md, requirements.txt, .gitignore, LICENSE (MIT,
Awais Ahmed Shah), COLAB_RUN_SHEET.md, BUILD_LOG.md, 3 executed notebooks, 6 figures,
model_metrics.csv, forecast_2026_2030.csv.

## What remains undone (and why)
- **PBS detailed tables** (province / gender / education breakdowns): not yet added.
  They were not reliably retrievable from the PBS website in this session; they must be
  verified cell-by-cell against published PBS tables before inclusion (next stage).
- **Dashboard:** listed as planned future work in the README/report; not built in this stage.
- **Pushing to GitHub:** intentionally not done here — staging only, per instructions.
  The `.venv/` folder is excluded via `.gitignore` and must not be committed.
