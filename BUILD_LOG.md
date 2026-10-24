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

## Stage 2 — PBS province panel + dashboard (25 Oct 2026, local staging only)

### Stage 2A — PBS LFS 2024-25 panel: DONE and verified
- **Source obtained:** the published PBS *Labour Force Survey 2024-25* Annual Report
  (37th round, September 2025, 205 pages) was downloaded from pbs.gov.pk
  (https://www.pbs.gov.pk/wp-content/uploads/2020/07/LFS-2024-25-Annual-Report.pdf,
  retrieved 25 Oct 2026, SHA-256
  79950b81ce4d738d48ff64f5e192f7905b112724a71b5d3018f4ff5991a57d48).
  An earlier session's failure to read PBS pages was a site-shell problem, not an
  absence of the report — the report PDF itself was directly retrievable.
- **Verification (two independent reads):** every table value was read once from the
  PDF text layer (pdftotext) and once from a rendered copy; the two reads agreed on
  every cell used. Values are transcribed exactly as published, including rounding
  quirks (rural Sindh female 2.5 < male 3.9 in Table 9.3; female Balochistan youth
  unemployed shown as 0.0m in Table 8.7). Nothing estimated, nothing borrowed.
- **Files added (124 data rows, each row carrying source report/table/URL):**
  `data/pbs_lfs_province_2024_25.csv` (Table 9.2, 19th ICLS),
  `data/pbs_lfs_province_region_2020_21_2024_25.csv` (Table 9.3, 13th ICLS),
  `data/pbs_lfs_youth_province_2024_25.csv` (Table 8.7, youth 15-24 × province × sex),
  `data/pbs_lfs_age_2024_25.csv` (Tables 9.4–9.6),
  `data/pbs_lfs_education_2024_25.csv` (Tables 9.7–9.8),
  `data/pbs_lfs_neet_2024_25.csv` (Table 8.8).
- **Notebook 04** (`notebooks/04_pbs_province_panel.ipynb`, 16 cells, executed with
  zero error outputs): integrity checks (no missing rates; spot-checks KP 9.6, KP
  female 18.1, Pakistan 7.1, KP female youth 25.6, Intermediate 12.6; youth counts
  consistent within 0.1m), gender gaps, youth-vs-all-ages ratios within the same
  framework/year, 2020-21 → 2024-25 change (13th ICLS only), and figures
  fig7_pbs_province_gender.png, fig8_pbs_youth_province.png, fig9_pbs_education.png
  (fig8 visually inspected: KP female youth bar 25.6% renders correctly).
- **Headline PBS findings:** KP worst overall (9.6%) and for youth (15.4%); survey
  youth 12.8% = 1.80× survey all-ages 7.1% (19th ICLS, same survey/year — a different
  method from the World Bank modelled 9.594%, never merged); KP female youth 25.6%
  highest cell; Punjab youth the only female-below-male case (12.6% vs 13.1%);
  education gradient rises with schooling (No Education 4.7% → Intermediate 12.6%)
  with degree females 24.1% vs males 7.0%; NEET improved nationally 32.5% → 28.4%
  but female NEET 45.4% vs male 13.0%.
- **Honest limits recorded in notebook 04 and the report:** youth-by-province exists
  only for 2024-25 (no published time series); no youth-by-education cross-tab is
  published (education = all ages); 19th vs 13th ICLS kept separate; survey ≠ modelled.

### Stage 2B — Interactive dashboard: DONE and verified
- **Files added:** `dashboard/app.py` (trend, model comparison, outlook, PBS panel —
  repo CSVs only), `dashboard/README.md`, `dashboard/requirements.txt`
  (streamlit, pandas, matplotlib).
- **Environment issue found and fixed honestly:** Streamlit's `st.dataframe`/`st.table`
  require pyarrow, which requires NumPy 2, while this project's analysis venv uses
  NumPy 1.26.4 (system scipy 1.11.4 is compiled for NumPy 1.x; upgrading NumPy to
  2.5.4 broke sklearn imports, so the upgrade was reverted and the venv restored to
  NumPy 1.26.4 with sklearn/statsmodels verified working again). Fix: tables render
  as Markdown via a helper in `app.py` — no pyarrow, works in every environment.
  This is documented in `app.py` itself.
- **Verification:** (1) Streamlit AppTest executed the full script with zero
  exceptions (12 markdown blocks rendered); (2) headless server started, main page
  returned HTTP 200, server log contained zero tracebacks; (3) server stopped
  cleanly afterwards (port 8501 closed, no stray processes).

### Stage 2C — Docs and final verification
- README.md: status "in progress" → "complete (Stage 1 + Stage 2)"; PBS panel and
  dashboard documented; structure and run instructions updated.
- report/research_report.md: status → complete; §3/§4 extended; new §5.4 (PBS panel);
  limitation 5 rewritten to the panel's real limits; §7 next steps marked done;
  full PBS citation (report, tables, URL, SHA-256) added to references.
- Notebooks 01–03: existing executed outputs confirmed intact (outputs present,
  no re-execution needed; the venv was restored to its stage-1 NumPy after the
  dashboard experiment above).
- **Not touched:** no GitHub login, no push, no browser window; `.venv/` remains
  excluded by `.gitignore` and appears in no upload list. Staging only — the push
  is a separate step requiring the owner's go-ahead and consent tap.

## What remains undone (and why)
- **Feature extension** (education-enrolment and sector indicators): future work only;
  not required for completion, and no public series for it was verified in this stage.
- **Pushing to GitHub:** intentionally not done here — staging only, per instructions.
  The `.venv/` folder is excluded via `.gitignore` and must not be committed.
