# Gazelle / Pon Bike – Marktanalyse en Dealernetwerk (Case)

Dit project helpt om in 2 dagen van ruwe data naar een board-ready advies te komen. We houden het simpel en stap-voor-stap. Geschikt voor junior data scientists.

## Doel
- Antwoord geven op: waar zijn we te veel / goed / weinig aanwezig?
- Hoe doet Pon (merken) het vs concurrenten?
- Waar liggen white spots (zonder goede dekking)?
- Wat leren we van Urban Arrow als benchmark?

## Data
- `dealer_lijst.csv`: winkels en merken. Eén winkel kan meerdere regels hebben (per merk). Unieke sleutel: `google_place_id`.
- `demografie.xlsx`: inwoners en demografie per postcode (CBS).

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
   - Excel inlezen (inwoners per postcode)
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
