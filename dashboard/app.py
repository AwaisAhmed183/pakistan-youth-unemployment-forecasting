"""Youth Unemployment in Pakistan — interactive dashboard (Streamlit).

Reads ONLY this repo's own CSVs (World Bank modelled series + published PBS
LFS 2024-25 tables). No new data, no estimates, no external calls at runtime.

Run from the repo root or from this folder:
    pip install -r dashboard/requirements.txt   (or: pip install streamlit pandas matplotlib)
    streamlit run dashboard/app.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
FIGSIZE = (10, 4.5)

def md_table(df):
    """Render a DataFrame as a Markdown table (no pyarrow dependency).

    Streamlit's st.dataframe/st.table require pyarrow, which requires NumPy 2,
    while this project's analysis environment uses NumPy 1.x (scipy/sklearn
    compatibility). Markdown tables render in every environment.
    """
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].round(3)
    header = "| " + " | ".join(map(str, d.columns)) + " |"
    sep = "| " + " | ".join(["---"] * len(d.columns)) + " |"
    rows = ["| " + " | ".join(str(v) for v in row) + " |" for row in d.values]
    st.markdown("\n".join([header, sep, *rows]))


st.set_page_config(page_title="Youth Unemployment in Pakistan", layout="wide")
st.title("Youth Unemployment in Pakistan")
st.write(
    "Final-year research dashboard — Awais Ahmed Shah, BS Data Science, UET Peshawar. "
    "Two kinds of evidence are shown, always labelled: **World Bank modelled ILO estimates** "
    "(1991–2025, notebooks 01–03) and **PBS household-survey figures** (LFS 2024-25, "
    "notebook 04). The two methods differ and are never merged into one series."
)

# ---------------------------------------------------------------- trend
st.header("1. Youth unemployment trend, 1991–2025 (World Bank, modelled ILO)")
wb = pd.read_csv(ROOT / "data" / "processed" / "pakistan_labour_indicators_1991_2025.csv")
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(wb["year"], wb["youth_unemployment_total"], label="Youth total (15-24)")
ax.plot(wb["year"], wb["youth_unemployment_male"], label="Youth male")
ax.plot(wb["year"], wb["youth_unemployment_female"], label="Youth female")
ax.plot(wb["year"], wb["unemployment_total"], label="All-ages total", linestyle="--")
ax.set_ylabel("Unemployment rate (%)")
ax.set_title("Pakistan — unemployment, World Bank modelled ILO estimates")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)
latest = wb.iloc[-1]
st.write(
    f"Latest year in the series: **{int(latest['year'])}** — youth total "
    f"**{latest['youth_unemployment_total']:.3f}%** (male {latest['youth_unemployment_male']:.3f}%, "
    f"female {latest['youth_unemployment_female']:.3f}%), all-ages total "
    f"{latest['unemployment_total']:.3f}%."
)

# ---------------------------------------------------------------- models
st.header("2. Model comparison (test years 2016–2025, one-step-ahead)")
metrics = pd.read_csv(ROOT / "results" / "model_metrics.csv")
md_table(metrics)
fig, ax = plt.subplots(figsize=FIGSIZE)
m = metrics.sort_values("MAE")
ax.barh(m["model"], m["MAE"])
ax.set_xlabel("Test MAE (percentage points)")
ax.set_title("Lower is better — Drift baseline beats every ML model on 35 annual points")
ax.grid(axis="x", alpha=0.3)
st.pyplot(fig)
st.write(
    "Honest result: the simple **Drift** baseline (MAE 0.886) beat ARIMA and both "
    "machine-learning models; Random Forest was worst (MAE 3.725). With only 35 annual "
    "observations, complex models overfit — the report says so plainly."
)

# ---------------------------------------------------------------- outlook
st.header("3. Outlook 2026–2030 (Drift baseline scenario)")
fc = pd.read_csv(ROOT / "results" / "forecast_2026_2030.csv")
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(wb["year"], wb["youth_unemployment_total"], label="Observed (World Bank, modelled)")
ax.plot(fc["year"], fc["forecast"], "r--", marker="o", label="Drift outlook 2026-2030")
ax.set_ylabel("Youth unemployment rate (%)")
ax.set_title("History and cautious 5-year outlook")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)
md_table(fc)
st.warning(
    "Uncertainty note: this outlook is a baseline scenario under 'recent patterns continue'. "
    "It is NOT a promise — no confidence interval is claimed, and one economic shock "
    "would move reality away from this line."
)

# ---------------------------------------------------------------- PBS
st.header("4. PBS province panel (LFS 2024-25, household survey)")
st.write(
    "Source: Pakistan Bureau of Statistics, *Labour Force Survey 2024-25*, 37th round, "
    "September 2025. Tables 9.2, 8.7 and 9.7. PBS stage status: **complete** — every "
    "value below was read from the published tables and cross-checked twice."
)
prov = pd.read_csv(ROOT / "data" / "pbs_lfs_province_2024_25.csv")
st.subheader("Unemployment by province and sex, all ages (19th ICLS)")
md_table(prov[["province", "unemployment_total", "unemployment_male",
                   "unemployment_female"]])
fig, ax = plt.subplots(figsize=FIGSIZE)
provs = ["KP", "Punjab", "Sindh", "Balochistan"]
x = range(len(provs))
w = 0.25
d = prov.set_index("province")
for i, col in enumerate(["unemployment_total", "unemployment_male", "unemployment_female"]):
    ax.bar([v + (i - 1) * w for v in x], [d.loc[p, col] for p in provs], w,
           label=["Total", "Male", "Female"][i])
ax.set_xticks(list(x))
ax.set_xticklabels(provs)
ax.set_ylabel("Unemployment rate (%)")
ax.set_title("PBS LFS 2024-25 — by province and sex (19th ICLS)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)

youth = pd.read_csv(ROOT / "data" / "pbs_lfs_youth_province_2024_25.csv")
st.subheader("Youth (15-24) unemployment by province and sex (19th ICLS)")
yd = youth[youth["province"] != "Total"].pivot(index="province", columns="sex",
                                              values="unemployment_rate")
md_table(yd)
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, col in enumerate(["Total", "Male", "Female"]):
    ax.bar([v + (i - 1) * w for v in x], [yd.loc[p, col] for p in provs], w, label=col)
ax.axhline(12.8, color="red", linestyle="--", linewidth=1, label="Pakistan youth 12.8%")
ax.set_xticks(list(x))
ax.set_xticklabels(provs)
ax.set_ylabel("Youth unemployment rate 15-24 (%)")
ax.set_title("PBS LFS 2024-25 — youth (15-24) by province and sex (19th ICLS)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
st.write(
    "Headlines: KP youth 15.4% is highest; KP females aged 15-24 reach **25.6%**, the "
    "highest cell in the panel. Punjab is the only province where youth females (12.6%) "
    "sit below youth males (13.1%)."
)

edu = pd.read_csv(ROOT / "data" / "pbs_lfs_education_2024_25.csv")
st.subheader("Unemployment by education level and sex, all ages (19th ICLS)")
e19 = edu[(edu["framework"] == "19th ICLS") & (edu["year"] == "2024-25")]
md_table(e19[["education_level", "unemployment_total", "unemployment_male",
                  "unemployment_female"]])
st.write(
    "Unemployment rises with schooling (no education 4.7% → intermediate 12.6%), and "
    "the gender gap at degree level is stark (females 24.1% vs males 7.0%). The "
    "education table covers all ages — PBS publishes no youth-by-education cross-tab "
    "in this report, so none is shown."
)

st.header("Sources and limits")
st.write(
    "- World Bank Open Data API (country PAK, 1991–2025, retrieved 23–24 Oct 2026; "
    "modelled ILO estimates) — see data/sources.md and notebooks 01–03.\n"
    "- PBS Labour Force Survey 2024-25, 37th round, September 2025 — Tables 9.2, 9.3, "
    "9.4, 9.5, 9.6, 9.7, 9.8, 8.7, 8.8 — see notebook 04 and data/pbs_lfs_*.csv "
    "(every CSV row carries its source table).\n"
    "- Limits: PBS youth-by-province exists only for 2024-25 (no published time series); "
    "education is all-ages; survey and modelled figures are never merged; the 2026–2030 "
    "outlook is an uncertain baseline scenario, not a forecast promise."
)
