"""Youth Unemployment in Pakistan — interactive dashboard (Streamlit).

Reads ONLY this repo's own CSVs (World Bank modelled series + published PBS
LFS 2024-25 tables). No new data, no estimates, no external calls at runtime.
Every chart is interactive (hover for values, drag to zoom) — no static pictures.

Run from the repo root or from this folder:
    pip install -r dashboard/requirements.txt   (or: pip install streamlit pandas plotly)
    streamlit run dashboard/app.py
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent

# Matplotlib's default colours, kept so the charts look the same as before.
BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"


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
fig = go.Figure()
fig.add_trace(go.Scatter(x=wb["year"], y=wb["youth_unemployment_total"],
                         mode="lines", name="Youth total (15-24)"))
fig.add_trace(go.Scatter(x=wb["year"], y=wb["youth_unemployment_male"],
                         mode="lines", name="Youth male"))
fig.add_trace(go.Scatter(x=wb["year"], y=wb["youth_unemployment_female"],
                         mode="lines", name="Youth female"))
fig.add_trace(go.Scatter(x=wb["year"], y=wb["unemployment_total"],
                         mode="lines", name="All-ages total",
                         line=dict(dash="dash")))
fig.update_layout(title="Pakistan — unemployment, World Bank modelled ILO estimates",
                  yaxis_title="Unemployment rate (%)",
                  hovermode="x unified")
st.plotly_chart(fig, width="stretch")
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
m = metrics.sort_values("MAE", ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(x=m["MAE"], y=m["model"], orientation="h", marker_color=BLUE))
fig.update_layout(title="Lower is better — Drift baseline beats every ML model on 35 annual points",
                  xaxis_title="Test MAE (percentage points)")
st.plotly_chart(fig, width="stretch")
st.write(
    "Honest result: the simple **Drift** baseline (MAE 0.886) beat ARIMA and both "
    "machine-learning models; Random Forest was worst (MAE 3.725). With only 35 annual "
    "observations, complex models overfit — the report says so plainly."
)

# ---------------------------------------------------------------- outlook
st.header("3. Outlook 2026–2030 (Drift baseline scenario)")
fc = pd.read_csv(ROOT / "results" / "forecast_2026_2030.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=wb["year"], y=wb["youth_unemployment_total"],
                         mode="lines", name="Observed (World Bank, modelled)"))
fig.add_trace(go.Scatter(x=fc["year"], y=fc["forecast"],
                         mode="lines+markers", name="Drift outlook 2026-2030",
                         line=dict(color="red", dash="dash")))
fig.update_layout(title="History and cautious 5-year outlook",
                  yaxis_title="Youth unemployment rate (%)",
                  hovermode="x unified")
st.plotly_chart(fig, width="stretch")
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
provs = ["KP", "Punjab", "Sindh", "Balochistan"]
d = prov.set_index("province")
fig = go.Figure()
for col, label, color in [("unemployment_total", "Total", BLUE),
                          ("unemployment_male", "Male", ORANGE),
                          ("unemployment_female", "Female", GREEN)]:
    fig.add_trace(go.Bar(x=provs, y=[d.loc[p, col] for p in provs],
                         name=label, marker_color=color))
fig.update_layout(barmode="group",
                  title="PBS LFS 2024-25 — by province and sex (19th ICLS)",
                  yaxis_title="Unemployment rate (%)")
st.plotly_chart(fig, width="stretch")

youth = pd.read_csv(ROOT / "data" / "pbs_lfs_youth_province_2024_25.csv")
st.subheader("Youth (15-24) unemployment by province and sex (19th ICLS)")
yd = youth[youth["province"] != "Total"].pivot(index="province", columns="sex",
                                              values="unemployment_rate")
md_table(yd)
fig = go.Figure()
for col, color in [("Total", BLUE), ("Male", ORANGE), ("Female", GREEN)]:
    fig.add_trace(go.Bar(x=provs, y=[yd.loc[p, col] for p in provs],
                         name=col, marker_color=color))
fig.add_hline(y=12.8, line_dash="dash", line_color="red",
              annotation_text="Pakistan youth 12.8%")
fig.update_layout(barmode="group",
                  title="PBS LFS 2024-25 — youth (15-24) by province and sex (19th ICLS)",
                  yaxis_title="Youth unemployment rate 15-24 (%)")
st.plotly_chart(fig, width="stretch")
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
