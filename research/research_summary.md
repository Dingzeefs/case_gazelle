## Research summary – network strategy, policy and portfolio

This note distills actionable insights from the attached research and maps them to our repository plan and deliverables.

### Sources reviewed

- Voorbeelden van Vergelijkbare Cases en Aanpakken (retail/store network examples; proximity and white‑space)
- Strategie van Urban Arrow en Pon.Bike – Succes, Uitbreiding en Portfolio‑Advies (UA strategy, B2C/B2B, international rollout)
- Cargo‑bike report ZEZ (Dutch Cycling Embassy) – zero‑emission zones timeline for cities
- Internal notes in `research/notes.md`

### Key takeaways we will use directly

- Competitive proximity and cannibalization
  - Track Pon↔non‑Pon competitors within 1/3/5 km; compare Pon↔Pon spacing.
  - Apply guardrails: minimum spacing by brand (UA 3–5 km; Gazelle 5–7.5 km) to reduce cannibalization.

- Policy‑aware prioritization (ZE/LEZ)
  - Build `policy_index` from `data/external/ze_steden.csv` (earlier start → higher weight).
  - Multiply white‑spot score by `(1 + α·policy_index)`; default α = 0.5.

- Demography integration (CBS)
  - Clean `demografie.csv` (−99997 → 0 for counts, NaN for ratios), normalize features.
  - Features: income (quantiles), households (size, 1p/with kids), age buckets, density, WOZ.
  - Cluster PC4s (4–6 segments) and report KPI deltas per cluster.

- White‑space at two scales
  - PC4 coverage and scoring as baseline.
  - Optional micro‑gaps with H3 grid (res 7–8) for dense cities.

- UA international rollout (B2C + B2B)
  - City score: density + modal share + ZE/LEZ timing + income + logistics POIs.
  - Start with 2–3 pilot cities; quality dealers first (service coverage), enforce spacing, target ≥80% coverage at 5–7.5 km.

- Portfolio direction
  - Focus on e‑bike/cargo segments aligned with policy and dense urban markets.
  - Consider inclusive/adaptive mobility as a future white space; avoid internal brand overlap.

### Mapping to this repo

- Data
  - `data/raw/dealer_lijst.csv`, `data/raw/demografie.csv`, mapping `data/external/pc4_gemeente.csv`, policy `data/external/ze_steden.csv`.
- Notebooks
  - `01_dataprep.ipynb`: clean dealers + demography; generate clusters; export `data/processed/*.parquet` and `outputs/tables/kpis_by_pc4_with_clusters.csv`.
  - `02_coverage.ipynb`: compute nearest distances, coverage, proximity KPIs; rank white‑spots with policy multiplier; export `outputs/tables/white_spots_with_policy.csv`, `outputs/tables/proximity_kpis.csv`.
  - `03_kpis_viz.ipynb`: figures and KPI tables; export `outputs/tables/kpi_overview.csv`.
  - `05_intl_shortlist.ipynb` (new): compute UA city score and pilots; export `outputs/tables/ua_intl_shortlist.csv`.
- App
  - `app/streamlit_app.py`: add KPI table, ZE‑toggle filter, optional choropleth by gemeente and cluster filter.

### KPIs to report

- Coverage (Pon, per brand) vs UA benchmark
- Dealers per 100k (total, Pon, per brand)
- Pon‑share and competitor intensity
- Proximity and cannibalization metrics (rings; average distances)
- White‑spots ranked, with and without policy multiplier; cluster breakdown
- UA international: city scores and pilot picks

### Next steps (technical)

1) Implement proximity KPIs and policy‑aware scoring in `02_coverage.ipynb` and export tables.
2) Add demography clusters in `01_dataprep.ipynb`; propagate to outputs.
3) Create `05_intl_shortlist.ipynb` for UA rollout (city score and pilots).
4) Extend Streamlit with KPI table, cluster filter, and (optional) choropleth.


