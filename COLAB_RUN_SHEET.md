# Colab Run Sheet

## Status: Colab is NOT needed

All three notebooks were **fully executed locally** on 24 Oct 2026 (see `BUILD_LOG.md`).
The notebooks in this repository are committed with their real outputs, the figures are
in `results/figures/`, and the metrics/forecast are in `results/`.

**An honest note about "training":** this project's dataset is *annual* — 35 rows.
Every model here (including the Random Forest) trains in seconds on any laptop CPU.
There is no heavy training in this project and no GPU is needed at any point. Colab is
only a spare execution route if a local machine is unavailable.

## Optional: re-run everything in Google Colab (verification / demo)

1. Go to https://colab.research.google.com/ and sign in.
2. Upload the project folder (or, after the repo is on GitHub, use
   *File → Open notebook → GitHub* and paste the repository URL).
3. Open `notebooks/01_data_collection.ipynb` → *Runtime → Run all*.
   (Internet is available in Colab, so it will fetch fresh World Bank data itself.)
4. Then run `notebooks/02_cleaning_and_eda.ipynb` → *Run all*.
5. Then run `notebooks/03_forecasting_models.ipynb` → *Run all*.
   If a package is missing, run this in a first cell: `!pip install -q statsmodels scikit-learn`
6. Download the refreshed outputs if you want them locally:
   `results/model_metrics.csv`, `results/forecast_2026_2030.csv`,
   and the PNGs in `results/figures/`.

Expected headline results of a successful re-run (from the local execution, 24 Oct 2026 —
small floating-point differences are normal):
- Youth unemployment 2025 = 9.594%; series peak 11.053% (2021)
- Test MAE ranking: Drift 0.886 < Naive 0.921 < ARIMA(2,1,0) 1.185 < Linear Regression 1.742 < Random Forest 3.725
