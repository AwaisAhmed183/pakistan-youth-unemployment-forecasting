# Dashboard — Youth Unemployment in Pakistan

Interactive Streamlit dashboard for this research project. It reads **only** this
repo's own CSVs — the World Bank modelled series (`data/processed/`) and the
published PBS LFS 2024-25 tables (`data/pbs_lfs_*.csv`). No new data, no estimates,
no network calls at runtime.

## What it shows
1. Youth unemployment trend 1991–2025 (World Bank, modelled ILO estimates)
2. Model comparison table and chart (test years 2016–2025)
3. Drift outlook 2026–2030, with the uncertainty warning
4. PBS province panel: unemployment by province × sex, youth (15-24) by province ×
   sex, and unemployment by education level (all ages)

Survey figures (PBS) and modelled figures (World Bank) are labelled separately
throughout and are never merged into one series.

## Run it
```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```
Then open the local URL Streamlit prints (usually http://localhost:8501).
To run from inside the `dashboard/` folder instead, use
`streamlit run app.py` — data paths are resolved from the file location, so both
work.

## Verify it runs
```bash
streamlit run dashboard/app.py --server.headless true --server.port 8501 &
curl -s http://localhost:8501/healthz   # expect: ok
```
