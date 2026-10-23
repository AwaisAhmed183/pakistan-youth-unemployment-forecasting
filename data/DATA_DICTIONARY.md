# Data Dictionary

Dataset: `data/processed/pakistan_labour_indicators_1991_2025.csv`
(and the identical, sorted copy `data/processed/pakistan_labour_clean.csv` produced by notebook 02)

- **Coverage:** Pakistan, one row per year, 1991–2025 (35 rows).
- **Missing values:** none — every column has a value for all 35 years (verified in notebook 02).
- **Producer of the underlying series:** World Bank Open Data, from ILO modelled estimates
  (see `data/sources.md` for exact indicator codes and retrieval details).

| Column | Meaning | Unit | Source code |
|---|---|---|---|
| `year` | Calendar year of the observation | year | — |
| `youth_unemployment_total` | Unemployment rate, youth total, ages 15–24 (% of the youth labour force) | % | SL.UEM.1524.ZS |
| `youth_unemployment_male` | Unemployment rate, youth male, ages 15–24 (% of the male youth labour force) | % | SL.UEM.1524.MA.ZS |
| `youth_unemployment_female` | Unemployment rate, youth female, ages 15–24 (% of the female youth labour force) | % | SL.UEM.1524.FE.ZS |
| `unemployment_total` | Unemployment rate, all ages (% of the total labour force) | % | SL.UEM.TOTL.ZS |
| `labour_force_participation_total` | Labour force participation rate, total (% of the population ages 15+) | % | SL.TLF.CACT.ZS |
| `gdp_per_capita_usd` | GDP per capita, current US dollars (not inflation-adjusted) | US$ | NY.GDP.PCAP.CD |

## Notes for anyone reusing this dataset

1. **Modelled, not raw.** The unemployment and participation columns are modelled ILO
   estimates as published by the World Bank. Treat early-1990s values (youth unemployment
   near 1%) with caution — they come from a period with very different measurement
   conditions and are not comfortably comparable with recent decades.
2. **Do not mix with PBS figures without saying so.** Pakistan Bureau of Statistics
   LFS 2024-25 reports 7.1% overall unemployment and 46.3% participation using its own
   survey methodology; the World Bank modelled series for 2025 shows 5.420% total
   unemployment and 52.335% participation (ages 15+). Both are legitimate; they are
   answers from different instruments and must be labelled when quoted.
3. **GDP per capita is nominal.** `gdp_per_capita_usd` is in current US$, so it moves with
   exchange rates as well as real growth; it is used in this project only as context,
   not as a forecasting input.
4. **Target variable.** All forecasting in notebook 03 uses `youth_unemployment_total`.
