# Gazelle / Pon Bike – Marktanalyse en Dealernetwerk (Case)

Dit project helpt om in 2 dagen van ruwe data naar een board-ready advies te komen. We houden het simpel en stap-voor-stap. Geschikt voor junior data scientists.

## Doel
- Antwoord geven op: waar zijn we te veel / goed / weinig aanwezig?
- Hoe doet Pon (merken) het vs concurrenten?
- Waar liggen white spots (zonder goede dekking)?
- Wat leren we van Urban Arrow als benchmark?

## Data
- `dealer_lijst.csv`: winkels en merken. Eén winkel kan meerdere regels hebben (per merk). Unieke sleutel: `google_place_id`.
- `demografie.csv`: inwoners en demografie per postcode (CBS).(dealers en merken in NL), (CBS-demografie per postcode) (inkomens, huishoudens, leeftijden, gezinnen etc)  Weet dat voor de data, betekenis -99997 =  '0 - 4 / geheim / niet aanwezig'.

## Kernbegrippen (simpele definities)
- **Dealer (uniek)**: één winkel (gebaseerd op `google_place_id`).
- **Pon-merken**: Gazelle, Cannondale, Union, Kalkhoff, Urban Arrow, Cervélo, Focus, Santa Cruz.
- **Coverage (dekking)**: % inwoners binnen een afstand (R km) van een dealer (Pon of merk-specifiek).
- **White spot**: gebied waar inwoners buiten R km van een Pon-dealer wonen.
- **Dealers per 100k inwoners**: #dealers / inwoners * 100000.
- **Pon-share**: #Pon-dealers / #alle dealers.
- **Concurrentie-intensiteit**: verhouding Pon vs niet-Pon dealers.

## KPI's die we rapporteren
- Dealers per 100k (totaal, Pon, per merk)
- Pon-share bij dealers (per regio)
- Coverage vs benchmark (Urban Arrow)
- White-spots: aantal en inwoners
- Concurrentie-intensiteit: Pon t.o.v. niet-Pon
 - Dealerkwaliteit (proxy): `avg_rating * log(1 + reviews)`

## Stappenplan
1) **Data inlezen en schoonmaken**
   - CSV inlezen, leegtes/duplicaten controleren
   - CSV inlezen (inwoners per postcode)
   - Unieke dealers maken: groeperen op `google_place_id`
   - Merkenlijst per dealer maken; Pon-vlag toevoegen

2) **Regio-koppeling**
   - Postcode aan gemeente/provincie koppelen (via referentietabel)
   - Inwoners per gemeente/provincie optellen

3) **KPI-berekening per regio**
   - Dealers per 100k (totaal, Pon, per merk)
   - Pon-share en concurrentie-intensiteit

4) **Coverage-model** (simpel, snel)
   - Voor elke postcode berekenen: afstand tot dichtstbijzijnde Pon-dealer en per merk
   - R (radius) start = 7.5 km overal
   - Coverage% = % inwoners binnen R van een Pon-dealer
   - White-spots = postcodes buiten R, som inwoners

5) **Urban Arrow benchmark**
   - UA-dealers selecteren
   - UA-coverage berekenen (zelfde methode)
   - Target afleiden (bv. 80% landelijk); vergelijken met Pon

6) **Over-/onderbediend label**
   - Vergelijk regio’s met NL-gemiddelde of UA-target
   - Onderbediend = duidelijk lager dan referentie; overbediend = duidelijk hoger

7) **Prioriteit white-spots**
   - Rangschik op: inwoners (hoog is beter), afstand tot Pon-dealer (ver is beter), weinig concurrentie
   - Top-gebieden met voorstel: nieuw openen of dealer converteren

8) **Visualisaties en dashboard**
   - Kaarten: choropleths (dealers/100k, coverage), puntenkaart dealers
   - Grafieken: bar (top onderbediende), scatter (coverage vs concurrentie)
   - Dashboard met filters: merk, regio (Streamlit)

9) **Slides (≤ 15 min)**
   - Waar staan we? (huidige positie)
   - Coverage en white-spots (impact)
   - Concurrentiepositie
   - Advies en roadmap (concrete vervolgstappen)

## Map-structuur
- `data/raw/`: originele data (CSV/XLSX)
- `data/processed/`: tussenresultaten
- `notebooks/`: analyses per stap
- `src/`: herbruikbare functies (geo, coverage, kpis)
- `outputs/`: figuren en tabellen
- `dashboard/`: dashboard-bestanden

## Benodigde Python-pakketten
Zie `requirements.txt`.

## Aannames en beperkingen
- Unieke dealer = `google_place_id`
- Afstand = hemelsbreed, geen reistijd
- R = 7.5 km (gevoeligheidsanalyse kan later)
- Data kan onvolledig zijn (ratings, adressen); we documenteren dit
 - Geen omzetclaims: we gebruiken publieke proxies (CBS inkomen, urbanisatie, modal split, ZE‑beleid)

## Next steps (technisch)
- Notebook `01_dataprep.ipynb`: inlezen, schoonmaken, koppelen
- Notebook `02_coverage.ipynb`: coverage + white-spots
- Notebook `03_kpis_viz.ipynb`: KPI’s, grafieken, tabellen
- Exporteer figuren/tabellen naar `outputs/`
- Bouw dashboard (Tableau/Power BI/Excel)
- Maak slides en lever op

## Beantwoording verplichte casevragen (wat en waar in dit plan)

- Over-/onder-/goed bediend: via `coverage` (R=7.5 km) en KPI’s per regio (dealers/100k, Pon‑share, concurrentie). Visuals: choropleths + white‑spots. Zie secties: Stappen 3–4–6–7 en “Visualisaties en dashboard”.
- Urban Arrow internationaal advies: UA als benchmark (stap 5) en framework in “Advies voor Urban Arrow – uitrol in vergelijkbaar land”. Focus op vergelijkbare stedelijke dichtheid en ZE/LEZ‑beleid.
- Portfolio-advies (stoppen/toevoegen) met CSR/policy: “Extra strategische onderdelen”, “Portfolio‑matrix”, en weging in prioriteringsscore. CSR/policy argumenten geborgd via ZE‑policy integratie (zie hieronder).

## Policy/ZE (Zero‑Emissie) integratie

- Bron: `data/external/ze_steden.csv` (uit Dutch Cycling Embassy‑rapport). Hieruit bouwen we `outputs/tables/policy_index.csv` met startdatum en `policy_index` per gemeente.
- Gebruik: `policy_index` weegt mee in white‑spot/prioriteringsscore (hogere score in ZE‑steden en vroege startjaren). Ook als kaartlaag (toggle) in dashboard/slides.
- Koppeling: gemeente‑niveau (optioneel PC4 indien mapping beschikbaar). Zie scripts: `src/build_policy_index.py`, `src/fetch_external.py` (hardened fetch, optioneel).

## UA‑international (data‑science, proxies en outputs)

- Doel: transfer van NL‑succes naar vergelijkbare steden/landen met publieke proxies (geen omzetclaims).
- Proxies per stad/metro: urbanisatie/dichtheid (Eurostat/OECD), ZE/LEZ‑beleid (policy‑flag), fiets‑modal share/bike‑friendliness (publieke index), inkomen/koopkracht (OECD/Eurostat), OSM/Overpass POIs (retail/HoReCa/logistics) en (proxy) fietsinfra‑dichtheid.
- Similarity‑score t.o.v. NL‑benchmark: w(dichtheid, policy, modal, inkomen, POI/infra). Resultaat: shortlist top‑N steden.
- Coverage‑simulatie: NL‑radius (5/7.5/10/12 km) → schatting #dealers tot target per stad; guardrails met proximity (kannibalisatie laag houden).
- Deliverables: `outputs/tables/ua_intl_shortlist.csv` (scores, policy‑flag, gap→#dealers); figuur (top‑steden); 3 pilotsteden + KPI’s.
- Notebook: `notebooks/05_intl_shortlist.ipynb` (fetch/scrape → score → export). 

## CSR en politieke overwegingen (hoe we dit meenemen)

- Definitie (praktisch): bijdrage aan emissiereductie (ZE/LEZ), stedelijke leefbaarheid/ruimte, duurzame mobiliteit, en lokale economische effecten (werkgelegenheid/servicecapaciteit). Politiek: alignment met gemeentelijke/transitie‑agenda’s.
- Model‑representatie: `policy_index` (ZE/LEZ) als expliciete feature; stedelijkheid/dichtheid als leefbaarheid/footfall‑proxy; proximity‑guardrails om overlast/saturatie te beperken.
- Gebruik in beslisboom: bij gelijke “data‑score” krijgt scenario met hogere CSR/policy‑waarde de voorkeur (bijv. UA in ZE‑stad). In portfolio‑advies kan een merk met lage incremental coverage maar hoge CSR‑waarde toch “behouden/opschalen” zijn in specifieke segmenten.

## Uitbreidingen op plan (onderzoek + techniek)

- Onderzoekssamenvattingen (Cargo‑bike/ZEZ, Urban Arrow, Pon.Bike):
  - In grote steden neemt de beleidsdruk (ZE/LEZ) snel toe. Prioriteer ZE‑steden en vroege startjaren in de uitrol; gebruik `policy_index` als vermenigvuldigingsfactor in de score.
  - Urban Arrow: premium en service‑intensief, focus op dichte stedelijke kernen; hanteer cannibalisatie‑guardrails door minimale afstand tussen UA‑dealers (bijv. 3–5 km ringen) te respecteren.
  - Portfolio‑differentiatie: merken bedienen verschillende doelgroepen. Gebruik merk‑specifieke radius in gevoeligheidsanalyse (UA 5–7.5 km; Gazelle 7.5–10 km; sportief 7.5–12 km).

- Datakwaliteit en cleaning (CBS‑demografie):
  - Waarde −99997 interpreteren als 0 (tellingen) of NaN (percentages/ratio’s); documenteer per kolom. Type‑coercion naar numeriek en drop van volledig missende PC4‑regels.
  - Deduplicatie dealers op `google_place_id`; normaliseer merken (`brand_clean`) en Pon‑vlag (`is_pon_dealer`).
  - Mapping `PC4 → gemeente` via `data/external/pc4_gemeente.csv` voor aggregaties en policy‑join.

- Scoring white‑spots (beleid‑aware):
  - Basisscore S = z(inwoners) + z(dist_nearest_pon_km) − z(concurrentie_intensiteit) + 0.5 · z(pon_share_gap).
  - Policy‑correctie: S_policy = S × (1 + α · policy_index), standaard α = 0.5. Exporteer naar `outputs/tables/white_spots_with_policy.csv`.
  - Guardrails: sla gebieden met extreem hoge dealer‑dichtheid nabij (overlap binnen 0–3–5 km ringen) lager aan om kannibalisatie te beperken.

- KPI’s uitgebreid:
  - Coverage (Pon en per merk), dealers/100k, Pon‑share, concurrentie‑intensiteit.
  - Dealerkwaliteit (proxy) = `avg_rating * ln(1 + reviews)`; stabiliteit/top‑10 uit `outputs/tables/top10_stability.csv`.
  - Proximity KPI’s: overlap per ring (0–3–5–7.5–10 km) en dichtstbijzijnde afstandsverdeling.

- Validatie en sanity checks:
  - Herbereken inwoners‑totaal per gemeente/provincie en vergelijk met CBS‑referentie; steekproef top‑20 white‑spots en dichtstbijzijnde dealerlocaties.
  - Kaart‑controle: visualiseer outliers (zeer grote afstand of onrealistisch hoge aantallen) voor handmatige review.

- Reproduceerbare run (quickstart):
  - Voer `notebooks/01_dataprep.ipynb` → `02_coverage.ipynb` → `03_kpis_viz.ipynb` uit, en run `src/build_policy_index.py` voor policy.
  - Start dashboard: `streamlit run app/streamlit_app.py` en filter op merk/radius; toggle ZE‑steden.

- Dashboard‑uitbreidingen:
  - Choropleth‑laag per gemeente (dealers/100k of coverage) en toggle voor ZE‑policy.
  - KPI‑tabel met download (CSV) en white‑spots top‑50 (policy‑aware).

- Beperkingen en risico’s (expliciet):
  - Hemelsbrede afstand; ratings en reviews incompleet; geocoding onnauwkeurig op adresniveau; snapshots in de tijd; geen omzetdata. Documenteer aannames per slide/notebook.

