### Technisch stappenplan (end-to-end, copy-pastebaar)

0) Setup

- Terminal
```bash
cd /Users/DINGZEEFS/Case_Gazelle_Pon
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

1) Data sanity check (optioneel)
```bash
python - << 'PY'
import pandas as pd
print(pd.read_csv('data/raw/dealer_lijst.csv', nrows=2).to_string(index=False))
print(pd.read_csv('data/raw/demografie.csv', nrows=2).to_string(index=False))
print(pd.read_csv('data/external/ze_steden.csv', nrows=5).to_string(index=False))
print(pd.read_csv('data/external/pc4_gemeente.csv', nrows=5).to_string(index=False))
PY
```

2) Notebook-run (non‑interactive)

- Dataprep
```bash
jupyter nbconvert --to notebook --execute notebooks/01_dataprep.ipynb --inplace
```
- Coverage + white‑spots + proximity
```bash
jupyter nbconvert --to notebook --execute notebooks/02_coverage.ipynb --inplace
```
- KPI’s & visuals
```bash
jupyter nbconvert --to notebook --execute notebooks/03_kpis_viz.ipynb --inplace
```
- (Optioneel) Enrichment
```bash
jupyter nbconvert --to notebook --execute notebooks/04_enrichment.ipynb --inplace
```
- UA shortlist (nieuw)
```bash
jupyter nbconvert --to notebook --execute notebooks/05_intl_shortlist.ipynb --inplace
```

3) Kernlogica per notebook (wat er minimaal in moet)

- 01_dataprep.ipynb
  - Lees `dealer_lijst.csv`; maak `brand_clean`, `is_pon_dealer` (merkenlijst in README), dedup op `google_place_id`.
  - Normaliseer postcode naar `pc4` (eerste 4 cijfers), schrijf `data/processed/dealers.parquet`.
  - Lees `demografie.csv`; vervang sentinel −99997 door NaN; zet komma‑decimalen om naar punt.
  - Map `pc4_gemeente.csv`; bouw features: population, households, 1p%, kids%, 25–44%, koop/huur, density, WOZ.
  - Cluster PC4’s (k=5) → kolom `cluster`; schrijf `data/processed/demografie.parquet` en `outputs/tables/kpis_by_pc4_with_clusters.csv`.

- 02_coverage.ipynb
  - Bepaal voor elke PC4 de afstand tot dichtstbijzijnde Pon‑dealer (haversine + KDTree).
  - Coverage per radius (5/7.5/10/12 km) → `outputs/tables/coverage_overall.csv`.
  - White‑spots (dist > 7.5 km) met inwoners + cluster → `outputs/tables/white_spots_ranked.csv`.
  - Policy‑aware score: join `outputs/tables/policy_index.csv` indien aanwezig, `score_policy = score*(1+0.5*policy_index)` → `outputs/tables/white_spots_with_policy.csv`.
  - Proximity KPI’s: Pon↔Pon en Pon↔non‑Pon counts in ringen (3/5/7.5/10 km) → `outputs/tables/proximity_kpis.csv`.
  - Demografie‑score S_dem bovenop policy (kids%, 25–44%, −1p%) → overschrijf/append in `white_spots_with_policy.csv`.

- 03_kpis_viz.ipynb
  - KPI per gemeente: `dealers`, `pon_dealers`, `dealers_per_100k`, `pon_share` → `outputs/tables/kpi_overview.csv`.
  - Combineer met white‑spots per gemeente; bereken `underserved_score`; export `outputs/tables/white_spots_top10_gemeenten.csv`.
  - Optioneel: figuren in `outputs/figures/`.

- 04_enrichment.ipynb (optioneel)
  - Koppel woonplaatsenbestand `data/external/Woonplaatsen_in_Nederland_*.csv` of `WoonplaatsenCodes.csv` indien nodig voor labels.

- 05_intl_shortlist.ipynb
  - Bouw eenvoudige stadentabel met proxies (density, modal share, policy, inkomen, logistics POIs).
  - Normaliseer 0..1, weeg tot `city_score`; stel target coverage 80% en schat `dealers_needed`.
  - Exporteer `outputs/tables/ua_intl_shortlist.csv` en toon top‑3.

4) Policy index genereren (eenmalig of updaten)
```bash
python src/build_policy_index.py
```

5) Streamlit dashboard
```bash
streamlit run app/streamlit_app.py
```
- Filters: Radius, Pon‑merken, ZE‑steden.
- White‑spots tabel laadt `white_spots_with_policy.csv` (fallback `white_spots_ranked.csv`).
- Verwachte kolommen: `pc4, gemeente, inwoners, dist_nearest_pon_km, score, policy_index, score_policy, S_dem`.

6) Deliverables voor presentatie (15 min)
- Tabellen mee te nemen uit `outputs/tables/`:
  - `white_spots_top10_gemeenten.csv` (Top‑10 onderbediend)
  - `kpi_overview.csv` (dealers/100k, pon_share per gemeente)
  - `proximity_kpis.csv` (cannibalisatie‑signalen per ring)
  - `ua_intl_shortlist.csv` (3 steden/landen met `city_score` en `dealers_needed`)
- Kaarten/figuren (optioneel): choropleth per gemeente + dealerspunten; bar van Top‑10.

7) Git commits
```bash
git add .
git commit -m "run notebooks; export KPIs and white-spots; add proximity and UA shortlist"
```
