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

---

Here’s a concrete, copy-pasteable execution plan a junior dev can follow end-to-end. It covers setup, notebooks, exports, and Streamlit. Follow it in order.

### 0) Project setup
- Create and activate a Python venv
```bash
cd /Users/DINGZEEFS/Case_Gazelle_Pon
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

- Quick data sanity (optional, helpful)
```bash
python - << 'PY'
import pandas as pd
print("Dealers:", pd.read_csv("data/raw/dealer_lijst.csv", nrows=3).head(2).to_string(index=False))
print("\nDemografie:", pd.read_csv("data/raw/demografie.csv", nrows=3).head(2).to_string(index=False))
print("\nPolicy:", pd.read_csv("data/external/ze_steden.csv").head(5).to_string(index=False))
print("\nPC4→Gemeente:", pd.read_csv("data/external/pc4_gemeente.csv").head(5).to_string(index=False))
PY
```

### 1) Notebook 01_dataprep.ipynb (dataprep, demografie + clusters)
Run non-interactively or open in Jupyter. For non-interactive:
```bash
jupyter nbconvert --to notebook --execute notebooks/01_dataprep.ipynb --inplace
```

If you need to create/complete the logic, these are the exact cells/steps to include.

- Imports and constants
```python
import pandas as pd, numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

RAW = Path("data/raw")
EXT = Path("data/external")
PROC = Path("data/processed")
OUT = Path("outputs/tables")
PROC.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

PON_BRANDS = {"gazelle","cannondale","union","kalkhoff","urban arrow","cervélo","cervelo","focus","santa cruz"}
```

- Load and clean dealers
```python
dealers = pd.read_csv(RAW/"dealer_lijst.csv")
dealers["brand_clean"] = dealers["brand"].fillna("").str.lower().str.strip()
dealers["is_pon_dealer"] = dealers["brand_clean"].isin(PON_BRANDS)
dealers = dealers.sort_values(["google_place_id","is_pon_dealer"], ascending=[True,False]).drop_duplicates("google_place_id")
dealers["postal_code"] = dealers["postal_code"].astype(str).str.replace(" ","", regex=False)
dealers["pc4"] = dealers["postal_code"].str[:4].str.extract(r"(\d{4})")[0]
dealers.to_parquet(PROC/"dealers.parquet", index=False)
```

- Load demografie (handle −99997), map PC4→gemeente, build features
```python
demo = pd.read_csv(RAW/"demografie.csv", dtype=str)
# Make headers safe
demo.columns = demo.columns.str.strip().str.replace("\n"," ", regex=False)
# Numeric columns: coerce and handle sentinel
for c in demo.columns[1:]:
    demo[c] = pd.to_numeric(demo[c].str.replace(",",".", regex=False), errors="coerce")
    demo[c] = demo[c].mask(demo[c]==-99997, np.nan)  # treat sentinel as NaN

demo = demo.rename(columns={"Postcode-4":"pc4"})
pc4_map = pd.read_csv(EXT/"pc4_gemeente.csv", dtype=str)
demo = demo.merge(pc4_map, on="pc4", how="left")

# Minimal feature set (adjust names to your CSV headers)
features = {
    "pop_total":"Totaal inwoners x1",
    "hh_total":"Totaal huishouden x1",
    "hh_1p":"Eenpersoons x1",
    "kids_0_15":"tot 15 jaar x1",
    "age_25_44":"25 tot 45 jaar x1",
    "koop_pct":"Koopwoning %",
    "huur_pct":"Huurwoning %",
    "density":"Omgevingsadressendichtheid adressen/km2",
    "woz":"WOZ-waarde woning x 1 000 Euro"
}
demo_feat = demo[["pc4","gemeente"] + list(features.values())].rename(columns={v:k for k,v in features.items()})

# Derive ratios
demo_feat["hh_1p_pct"] = demo_feat["hh_1p"] / demo_feat["hh_total"]
demo_feat["kids_0_15_pct"] = demo_feat["kids_0_15"] / demo_feat["pop_total"]
demo_feat["age_25_44_pct"] = demo_feat["age_25_44"] / demo_feat["pop_total"]

# Cluster PC4s (k=5 example)
X = demo_feat[["hh_1p_pct","kids_0_15_pct","age_25_44_pct","koop_pct","huur_pct","density","woz"]].astype(float).fillna(0.0)
X_scaled = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=5, n_init=10, random_state=42)
demo_feat["cluster"] = kmeans.fit_predict(X_scaled)

demo_feat.to_parquet(PROC/"demografie.parquet", index=False)
demo_feat.to_csv(OUT/"kpis_by_pc4_with_clusters.csv", index=False)
```

- Quick exports by gemeente (used later)
```python
by_gm = demo_feat.groupby("gemeente", dropna=False).agg(pop_total=("pop_total","sum"))
by_gm.to_csv(OUT/"kpis_by_pc4.csv", index=False)
```

### 2) Notebook 02_coverage.ipynb (coverage, proximity, white-spots)
Run:
```bash
jupyter nbconvert --to notebook --execute notebooks/02_coverage.ipynb --inplace
```

Core cells to include:

- Imports and load
```python
import pandas as pd, numpy as np
from pathlib import Path
from scipy.spatial import cKDTree
PROC = Path("data/processed"); OUT = Path("outputs/tables")

dealers = pd.read_parquet(PROC/"dealers.parquet")
demo = pd.read_parquet(PROC/"demografie.parquet")  # has pc4, gemeente, pop_total, cluster, etc.

# For PC4 centroids you may use dealers median coords by pc4 as proxy if true centroids missing
pc4_coords = dealers.dropna(subset=["pc4","google_lat","google_lng"]) \
    .groupby("pc4")["google_lat","google_lng"].median().rename(columns={"google_lat":"lat","google_lng":"lng"})
pc4 = demo.merge(pc4_coords, on="pc4", how="left").dropna(subset=["lat","lng"])
```

- Distance helpers (haversine) and nearest Pon dealer
```python
R_EARTH = 6371.0
def hav_km(lat1, lng1, lat2, lng2):
    p = np.pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p)*np.cos(lat2*p)*(1-np.cos((lng2-lng1)*p))/2
    return 2*R_EARTH*np.arcsin(np.sqrt(a))

pon = dealers[dealers["is_pon_dealer"] & dealers["google_lat"].notna() & dealers["google_lng"].notna()].copy()
pon_coords = pon[["google_lat","google_lng"]].to_numpy()
tree = cKDTree(np.deg2rad(pon_coords))  # use radian space; approximate for speed

pc4_rad = np.deg2rad(pc4[["lat","lng"]].to_numpy())
dist_rad, idx = tree.query(pc4_rad, k=1)
# Convert angular distance to km via small-angle approx
def rad_to_km(rad): return rad * R_EARTH
pc4["dist_nearest_pon_km"] = rad_to_km(dist_rad)
```

- Coverage by radius and white-spots
```python
RADII = [5.0, 7.5, 10.0, 12.0]
coverage_rows = []
for r in RADII:
    covered = pc4.loc[pc4["dist_nearest_pon_km"]<=r, "pop_total"].sum()
    total = pc4["pop_total"].sum()
    coverage_rows.append({"radius_km":r, "covered_pop":int(covered), "total_pop":int(total), "coverage_pct":covered/total if total else np.nan})
pd.DataFrame(coverage_rows).to_csv(OUT/"coverage_overall.csv", index=False)

white = pc4[pc4["dist_nearest_pon_km"]>7.5][["pc4","gemeente","pop_total","dist_nearest_pon_km","cluster"]].copy()
white = white.rename(columns={"pop_total":"inwoners"})
white["score"] = white["inwoners"].rank(pct=True) + white["dist_nearest_pon_km"].rank(pct=True)
white.to_csv(OUT/"white_spots_ranked.csv", index=False)
```

- Policy-aware score (if `policy_index` exists)
```python
try:
    pol = pd.read_csv(OUT/"policy_index.csv")
    white = white.merge(pol[["gemeente","policy_index"]], on="gemeente", how="left")
    alpha = 0.5
    white["score_policy"] = white["score"] * (1 + alpha * white["policy_index"].fillna(0))
    white.to_csv(OUT/"white_spots_with_policy.csv", index=False)
except Exception:
    pass
```

- Proximity KPIs and cannibalisatie rings
```python
def ring_counts(points_a, points_b, rings_km=(3,5,7.5,10)):
    a_rad = np.deg2rad(points_a[["google_lat","google_lng"]].to_numpy())
    b_rad = np.deg2rad(points_b[["google_lat","google_lng"]].to_numpy())
    tree_b = cKDTree(b_rad)
    rows=[]
    for r in rings_km:
        # Convert ring radius to radians
        rad = r / R_EARTH
        cnt = tree_b.query_ball_point(a_rad, r=rad)
        rows.append(sum(len(c)-1 for c in cnt))  # exclude self if same set
    return rows

pon_only = dealers[dealers["is_pon_dealer"] & dealers["google_lat"].notna()]
nonpon = dealers[(~dealers["is_pon_dealer"]) & dealers["google_lat"].notna()]

rings = (3,5,7.5,10)
kpi = {
    "pon_pon_counts": ring_counts(pon_only, pon_only, rings),
    "pon_nonpon_counts": ring_counts(pon_only, nonpon, rings)
}
prox = pd.DataFrame({"ring_km":rings, "pon_near_pon":kpi["pon_pon_counts"], "pon_near_nonpon":kpi["pon_nonpon_counts"]})
prox.to_csv(OUT/"proximity_kpis.csv", index=False)
```

- Demography-augmented score (S_dem)
```python
white = white.merge(pc4[["pc4","hh_1p_pct","kids_0_15_pct","age_25_44_pct"]], on="pc4", how="left")
for c in ["inwoners","dist_nearest_pon_km","hh_1p_pct","kids_0_15_pct","age_25_44_pct"]:
    white[f"z_{c}"] = (white[c]-white[c].mean())/white[c].std(ddof=0)
white["S_dem"] = white["score_policy"].fillna(white["score"]) \
    + 0.4*white["z_kids_0_15_pct"].fillna(0) + 0.4*white["z_age_25_44_pct"].fillna(0) - 0.2*white["z_hh_1p_pct"].fillna(0)
white.sort_values("S_dem", ascending=False).to_csv(OUT/"white_spots_with_policy.csv", index=False)
```

### 3) Notebook 03_kpis_viz.ipynb (KPI’s en visuals)
Run:
```bash
jupyter nbconvert --to notebook --execute notebooks/03_kpis_viz.ipynb --inplace
```

Core cells to include:

- Dealers per gemeente, Pon-share, top‑10 over/onder
```python
import pandas as pd, numpy as np
from pathlib import Path
PROC = Path("data/processed"); OUT = Path("outputs/tables"); FIG = Path("outputs/figures")
FIG.mkdir(parents=True, exist_ok=True)

dealers = pd.read_parquet(PROC/"dealers.parquet")
demo = pd.read_parquet(PROC/"demografie.parquet")["pc4","gemeente","pop_total"]
pc4counts = dealers.groupby("pc4").size().rename("dealers_pc4").reset_index()
gm = demo.groupby("gemeente", dropna=False).agg(pop=("pop_total","sum")).reset_index()
gm_dealers = dealers.groupby("gemeente", dropna=False).agg(dealers=("google_place_id","nunique"),
                                                           pon_dealers=("is_pon_dealer","sum")).reset_index()
gm_kpi = gm.merge(gm_dealers, on="gemeente", how="left").fillna(0)
gm_kpi["dealers_per_100k"] = gm_kpi["dealers"] / gm_kpi["pop"] * 100000
gm_kpi["pon_share"] = np.where(gm_kpi["dealers"]>0, gm_kpi["pon_dealers"]/gm_kpi["dealers"], np.nan)
gm_kpi.to_csv(OUT/"kpi_overview.csv", index=False)

# Top-10 onderbediend: laag dealers/100k, lage coverage, grote pop
cov = pd.read_csv(OUT/"coverage_overall.csv")
white = pd.read_csv(OUT/"white_spots_with_policy.csv", dtype={"pc4":str}) if (OUT/"white_spots_with_policy.csv").exists() else pd.read_csv(OUT/"white_spots_ranked.csv", dtype={"pc4":str})
white_gm = white.groupby("gemeente", dropna=False).agg(inwoners_white=("inwoners","sum"),
                                                       mean_dist=("dist_nearest_pon_km","mean"),
                                                       score=("score_policy","max")).reset_index()
final_gm = gm_kpi.merge(white_gm, on="gemeente", how="left").fillna({"inwoners_white":0,"mean_dist":0})
# crude composite to rank under-served
final_gm["underserved_score"] = (-final_gm["dealers_per_100k"].rank(pct=True)
                                 + final_gm["inwoners_white"].rank(pct=True)
                                 + final_gm["mean_dist"].rank(pct=True))
top10_under = final_gm.sort_values("underserved_score", ascending=False).head(10)
top10_under.to_csv(OUT/"white_spots_top10_gemeenten.csv", index=False)
```

- Optional: plots saved to `outputs/figures` (skip here for brevity)

### 4) Notebook 04_enrichment.ipynb (optional joins)
- If needed, join `Woonplaatsen_in_Nederland_2024_*.csv` for extra metadata. Otherwise you can skip.
```bash
jupyter nbconvert --to notebook --execute notebooks/04_enrichment.ipynb --inplace
```

### 5) Notebook 05_intl_shortlist.ipynb (UA international shortlist)
Create and run:
```bash
jupyter nbconvert --to notebook --execute notebooks/05_intl_shortlist.ipynb --inplace
```

Core cells to include:

- Build simple city dataset and score
```python
import pandas as pd, numpy as np
from pathlib import Path
OUT = Path("outputs/tables"); OUT.mkdir(parents=True, exist_ok=True)

# Example seed. Replace with real proxies when available.
cities = pd.DataFrame([
    {"country":"DE","city":"Berlin","density":4100,"modal_share_bike":0.18,"policy_flag":1.0,"income_idx":1.0,"logistics_poi_idx":0.9},
    {"country":"DK","city":"Copenhagen","density":7000,"modal_share_bike":0.35,"policy_flag":1.0,"income_idx":1.1,"logistics_poi_idx":0.8},
    {"country":"DE","city":"Munich","density":4800,"modal_share_bike":0.18,"policy_flag":0.7,"income_idx":1.2,"logistics_poi_idx":0.8},
    {"country":"BE","city":"Brussels","density":5200,"modal_share_bike":0.05,"policy_flag":0.7,"income_idx":1.0,"logistics_poi_idx":0.8},
    {"country":"FR","city":"Paris","density":21000,"modal_share_bike":0.07,"policy_flag":0.8,"income_idx":1.1,"logistics_poi_idx":1.0},
])
# Normalize 0..1
for c in ["density","modal_share_bike","policy_flag","income_idx","logistics_poi_idx"]:
    v = cities[c].astype(float)
    cities[f"z_{c}"] = (v - v.min())/(v.max()-v.min() + 1e-9)

w = {"density":0.25,"modal_share_bike":0.25,"policy_flag":0.25,"income_idx":0.1,"logistics_poi_idx":0.15}
cities["city_score"] = sum(w[k]*cities[f"z_{k}"] for k in w)
# Simple coverage gap model with placeholder current coverage
cities["coverage_current"] = 0.40  # replace if known per city
cities["coverage_target"] = 0.80
cities["gap"] = (cities["coverage_target"] - cities["coverage_current"]).clip(lower=0)
# Estimate dealers needed (assume 1 dealer lifts coverage by 0.01 → tune per brand)
lift_per_dealer = 0.01
cities["dealers_needed"] = np.ceil(cities["gap"] / lift_per_dealer).astype(int)

cities.sort_values("city_score", ascending=False).to_csv(OUT/"ua_intl_shortlist.csv", index=False)
```

- Present top‑3 cities by `city_score` with `dealers_needed`.

### 6) Build or refresh Policy Index (if missing)
```bash
python src/build_policy_index.py
```

### 7) Streamlit dashboard
- Run
```bash
streamlit run app/streamlit_app.py
```

- App behavior:
  - Map of dealers with brand filter.
  - White-spots table uses `outputs/tables/white_spots_with_policy.csv` if present; else falls back to `white_spots_ranked.csv`.
  - Toggle “ZE‑steden” filters by `policy_index` (>= 0.8).
  - Extend columns displayed by ensuring the following exports exist:
    - `white_spots_with_policy.csv` with columns like `pc4, gemeente, inwoners, dist_nearest_pon_km, score, policy_index, score_policy, S_dem`
    - `proximity_kpis.csv` with `ring_km, pon_near_pon, pon_near_nonpon`

### 8) Slides (15‑min deliverables)
- Pull tables:
  - `outputs/tables/white_spots_top10_gemeenten.csv` (Top‑10 onderbediend)
  - `outputs/tables/ua_intl_shortlist.csv` (3 steden/landen + dealers_needed)
  - `outputs/tables/kpi_overview.csv` (dealers/100k, pon_share per gemeente)
  - `outputs/tables/proximity_kpis.csv` (cannibalisatie signalen)
- Recommended visuals:
  - Choropleth per gemeente (coverage or dealers/100k) and points for dealers.
  - Bar: Top‑10 onderbediend gemeenten (composite score).
  - Table: 3 UA steden met `city_score`, `dealers_needed`.

### 9) Git hygiene
```bash
git add .
git commit -m "feat: refresh notebooks outputs; add proximity KPIs, policy-aware white-spots, UA shortlist"
```

### 10) Common pitfalls + fixes
- If `demografie.csv` parsing fails (comma decimals/newlines in headers):
  - Use `encoding="utf-8"` and `sep=","` explicitly; strip headers as shown; replace commas with dots before numeric coercion.
- If PC4 lat/lng missing:
  - Use median of dealer coordinates per `pc4` as proxy (as scripted) or provide a PC4 centroid file.
- If Streamlit shows “Run notebooks…”:
  - Ensure the CSVs exist in `outputs/tables` with exact filenames used by `app/streamlit_app.py`.
- If `policy_index.csv` missing:
  - Run `src/build_policy_index.py` or temporarily set `ze_only` toggle off.

That’s it. Start at step 0, then run 1→5 (and 6 if needed), then 7 for the dashboard, and assemble slides in 8 using the generated tables.

## Extra inspiratie (direct toepasbaar, zonder scraping of ML)

- Competitive co‑location & proximity‑visuals
  - Maak in `02_coverage.ipynb` een extra export `outputs/tables/proximity_report.csv` met:
    - Ringen: 1/3/5/7.5/10 km
    - `pon_near_pon`, `pon_near_nonpon` (non‑Pon = uit `dealer_lijst.csv` gefilterd via `is_pon_dealer == False`)
  - Voeg histogram van afstanden toe (Pon↔Pon en Pon↔non‑Pon) naar `outputs/figures/`.

- Cannibalisatie‑guardrails (per merk)
  - Stel minimale afstandsregels in (bijv. UA ≥3–5 km; Gazelle ≥5–7.5 km).
  - Voeg een penalty toe in white‑spot scoring wanneer een nieuwe dealer voorstel binnen de merk‑ring te veel Pon‑buren heeft.
  - Rapporteer per merk de ratio `pon_near_pon / pon_near_nonpon` per ring.

- H3 white‑space in steden (micro‑gaten)
  - Gebruik `h3` Python package en maak raster (res 7–8) voor drie grootste steden.
  - Aggregatie per cel: inwoners (gesommeerd via pc4→cel), min. afstand tot Pon‑dealer, count Pon/non‑Pon dealers per cel.
  - Exporteer top‑N cellen als `outputs/tables/white_spots_h3_{stad}.csv` en optionele folium‑kaart.

- Dealers/100k choropleth (Maptitude‑stijl)
  - In `03_kpis_viz.ipynb`: maak choropleth per gemeente met `dealers_per_100k` en aparte laag voor `pon_share`.
  - Sla PNG/HTML op naar `outputs/figures/` en verwijs in slides.

- UA benchmark‑curves
  - Plot coverage vs #Pon‑dealers (landelijk en per grote stad) en markeer target (80%).
  - Slide: “Gap → #dealers” voor 3 UA‑steden uit `ua_intl_shortlist.csv`.

### Extra inspiratie uit enrichment-snippet

- Enrichment naar white‑spots:
  - Merge demografische proxies zoals `income_norm`, `density_norm` (uit `demografie.parquet`) in `white_spots_ranked.csv` op `pc4`.
  - Map `pc4 → gemeente` via `data/external/pc4_gemeente.csv`; schoon `gemeente` met `.str.strip()`.
  - Optionele `plaats` toekenning:
    - Gebruik eigen `custom_pc4_plaats` dict voor edge‑cases (bijv. `7351: Hoenderloo`).
    - Fallback: neem primaire woonplaats per gemeente uit `Woonplaatsen_in_Nederland_2024_*.csv` (mode per gemeente); anders `gemeente` als `plaats`.
  - Policy: merge `ze_steden.csv` en zet `policy_index = 1.0` voor ZE‑gemeenten; overige `0.0`.
  - Herbereken `score` met gewichten (voorbeeld): `0.30·pop_norm + 0.20·dist_norm + 0.20·policy + 0.15·income_norm + 0.15·density_norm` en sorteer.
  - Exporteer als `outputs/tables/white_spots_with_policy.csv` met kolommen `pc4, gemeente, plaats, inwoners_pc4, dist_nearest_pon_km, income_norm, density_norm, policy_index, score`.

- Proximity quick‑wins (board‑ready):
  - Gebruik `BallTree` (haversine) met Pon‑coördinaten voor 300m Pon↔Pon en 500m Pon↔niet‑Pon flags.
  - Agregeer per `gemeente`: `pon_pon_300m_frac`, `pon_nonpon_500m_frac`, en `pon_count`; exporteer `outputs/tables/proximity_summary.csv`.
  - Maak een HTML‑kaart met ringen (300m/500m) rond eerste 300 Pon‑dealers → `outputs/figures/proximity_rings.html`.

- Robuuste PC4‑centroids:
  - Gebruik `pgeocode` om PC6‑gebaseerde lat/lng te benaderen voor elke PC4 (probeer `AA`, `AB` suffix); indien nodig fallback: gemiddelde van alle PC6 binnen PC4 uit pgeocode‑tabel.
  - Indien nog ontbrekend: gebruik gemiddelde dealer‑coördinaten per PC4 als noodoplossing.
  - Herbereken coverage (`coverage_overall.csv`) en white‑spots (`white_spots_ranked.csv`) met deze centroids.

---

## Notebook checklists (wat MOET erin) en verplichte exports

- 01_dataprep.ipynb
  - [ ] Dealers: `brand_clean`, `is_pon_dealer`, unieke `google_place_id`, `pc4` (4 cijfers), schrijf `data/processed/dealers.parquet`.
  - [ ] Demografie: sentinel −99997 → NaN; kolommen naar numeriek; join `pc4_gemeente.csv`.
  - [ ] Features & proxies:
    - `pop_total` (alias ook `inwoners` voor latere merge)
    - `density` (= Omgevingsadressendichtheid), `woz` (= WOZ‑waarde)
    - Norms: `income_norm = (woz - min)/(max - min)`, `density_norm` idem
    - Ratios: `hh_1p_pct`, `kids_0_15_pct`, `age_25_44_pct`
  - [ ] Clusters (k=5): voeg `cluster` toe
  - [ ] Exports: `data/processed/demografie.parquet`, `outputs/tables/kpis_by_pc4_with_clusters.csv`

- 02_coverage.ipynb
  - [ ] PC4‑coördinaten (median dealer per pc4 of centroids indien beschikbaar)
  - [ ] Afstand tot dichtstbijzijnde Pon‑dealer (haversine/KDTree)
  - [ ] Coverage radii tabel → `outputs/tables/coverage_overall.csv`
  - [ ] White‑spots (R=7.5 km) → `outputs/tables/white_spots_ranked.csv`
  - [ ] Policy‑aware score join (`policy_index.csv`) → `outputs/tables/white_spots_with_policy.csv`
  - [ ] Demografie‑score `S_dem` toevoegen (kids/25‑44 plus, 1p min) en wegschrijven naar dezelfde CSV
  - [ ] Proximity exports:
    - ringen (3/5/7.5/10 km) → `outputs/tables/proximity_kpis.csv`
    - 300m Pon↔Pon en 500m Pon↔niet‑Pon per gemeente → `outputs/tables/proximity_summary.csv`
    - optioneel ring‑kaart → `outputs/figures/proximity_rings.html`

- 03_kpis_viz.ipynb
  - [ ] `kpi_overview.csv` per gemeente: dealers, pon_dealers, dealers_per_100k, pon_share
  - [ ] Top‑10 onderbediend én top‑10 overbediend gemeenten exporteren:
    - Onderbediend: lage dealers/100k + veel inwoners_white + hoge mean_dist → `white_spots_top10_gemeenten.csv`
    - Overbediend: hoge dealers/100k + lage inwoners_white → `over_served_top10_gemeenten.csv`
  - [ ] Portfolio/merk‑KPI’s: per `brand_clean` dealers_per_100k en share (tabel) → `brand_counts_top20.csv` (of vergelijkbare export)
  - [ ] (Optioneel) Choropleths/figuren naar `outputs/figures/`

- 05_intl_shortlist.ipynb
  - [ ] City score tabel → `outputs/tables/ua_intl_shortlist.csv` (met `city_score`, `coverage_current`, `coverage_target`, `dealers_needed`)
  - [ ] Slide‑ready top‑3 selectie met target‑gap → #dealers

- Validatie (einde)
  - [ ] Bestaan en niet‑lege CSV’s: `coverage_overall.csv`, `white_spots_with_policy.csv`, `kpi_overview.csv`, `white_spots_top10_gemeenten.csv`, `proximity_kpis.csv`, `proximity_summary.csv`, `ua_intl_shortlist.csv`
  - [ ] Random seeds ingesteld (bijv. `random_state=42`) waar van toepassing
  - [ ] Kolomnamen consistent: `pc4`, `gemeente`, `inwoners`, `dist_nearest_pon_km`, `policy_index`, `S_dem`


