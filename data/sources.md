# Data Sources

All data in this project is public and used for non-commercial academic research.
Every number in the notebooks and report traces back to one of the sources below.

## 1. World Bank Open Data (main dataset)

- **Portal:** https://data.worldbank.org/
- **API base:** https://api.worldbank.org/v2/country/PAK/indicator/<CODE>?date=1991:2025&per_page=100&format=json
- **Country:** Pakistan (PAK) · **Years:** 1991–2025 · **Retrieved:** 23–24 Oct 2026
- **API last-updated stamp in responses:** 2026-10-08 (World Bank database update)

| Indicator code | Series | 2025 value (as fetched) |
|---|---|---|
| SL.UEM.1524.ZS | Unemployment, youth total (% of total labor force ages 15-24) (modeled ILO estimate) | 9.594 |
| SL.UEM.1524.MA.ZS | Unemployment, youth male (% of male labor force ages 15-24) (modeled ILO estimate) | 9.416 |
| SL.UEM.1524.FE.ZS | Unemployment, youth female (% of female labor force ages 15-24) (modeled ILO estimate) | 10.143 |
| SL.UEM.TOTL.ZS | Unemployment, total (% of total labor force) (modeled ILO estimate) | 5.420 |
| SL.TLF.CACT.ZS | Labor force participation rate, total (% of total population ages 15+) (modeled ILO estimate) | 52.335 |
| NY.GDP.PCAP.CD | GDP per capita (current US$) | 1595.909 |

Files produced from these responses:
- `data/raw/wb_<CODE>.json` — the raw API responses, exactly as returned.
- `data/raw/worldbank_pakistan_long.csv` — the same values transcribed into long format.
- `data/processed/pakistan_labour_indicators_1991_2025.csv` — wide analysis table.

**Important interpretation note:** the World Bank unemployment and participation series
above are *modelled ILO estimates*. They are designed for cross-country comparability and
do **not** have to match Pakistan's own survey figures below — the methods and reference
populations differ (e.g. the World Bank participation series covers ages 15+, modelled).

## 2. Pakistan Bureau of Statistics (PBS) — Labour Force Survey 2024-25

- **Website:** https://www.pbs.gov.pk/
- **Publication:** Labour Force Survey 2024-25 (Pakistan Bureau of Statistics, Government of Pakistan)

Headline figures verified from PBS for this project (checked on pbs.gov.pk, Oct 2026):

| Figure | Value |
|---|---|
| Overall unemployment rate, LFS 2024-25 | **7.1%** |
| Labour force participation rate, LFS 2024-25 | **46.3%** |

These PBS figures come from Pakistan's own household labour-force survey and are the
national reference point used in the research question and report. Detailed PBS tables
(province / gender / education breakdowns) are planned as a second data stage; any figure
from them will only be added to this project after it has been verified against the
published PBS tables, and it will be recorded here with its table reference.

## 3. Prior work referenced (method background)

- CodeAlpha_Unemployment_Analysis (author's internship project, Python/Pandas EDA on
  unemployment data): https://github.com/AwaisAhmed183/CodeAlpha_Unemployment_Analysis
  — its stated future work (apply ML models for prediction; build a dashboard) is what
  this project carries out, now on Pakistan data.
