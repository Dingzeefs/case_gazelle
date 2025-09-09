# Pon Bike Nederland - Dealer Network Analysis

Een data science case voor het analyseren van het fietsdealer netwerk in Nederland. Het project onderzoekt waar Pon te veel, goed of juist weinig aanwezig is en geeft strategisch advies over het dealernetwerk.

## Wat zit er in dit project

Het project analyseert 2,080 fietswinkels in Nederland waarvan 978 Pon dealers zijn. We kijken naar dekking, concurrentie, white spots en geven advies voor internationale expansie en portfolio strategie.

### Belangrijke bevindingen
- Marktaandeel: 22.3% (op basis van brand-dealer relaties)
- Coverage: 97.2% van de bevolking binnen 7.5km van een Pon dealer
- White spots: 66 gebieden met 289k inwoners ondervertegenwoordigd
- Multi-brand realiteit: 67.5% van alle dealers verkoopt meerdere merken

## Data bronnen

**Raw data (data/raw/)**
- `dealer_lijst.csv` - 6,748 brand-dealer relaties met Google Places data
- `demografie.csv` - CBS demografische data voor 4,073 postcodegebieden
- Let op: CBS waarde -99997 betekent missing/geheim

**External data (data/external/)**
- `Woonplaatsen_in_Nederland_2024.csv` - Plaats naar gemeente/provincie mapping
- `ze_steden.csv` - 29 steden met zero-emissie zones (2025-2028)

## Notebooks uitleg

### 01_dataprep.ipynb
**Wat doet het:** Maakt schone datasets van de ruwe dealer en demografische data.

**Belangrijkste stappen:**
1. Leest dealer_lijst.csv en verwijdert duplicaten op basis van google_place_id
2. Identificeert Pon merken (Gazelle, Urban Arrow, Cannondale, etc.)
3. Aggregeert multi-brand dealers naar unieke locaties
4. Koppelt demografische data aan postcodes
5. Maakt clustering van 5 demografische segmenten

**Output:**
- `dealers.parquet` - 2,080 unieke dealer locaties
- `dealers_all_brands.parquet` - 6,748 brand-dealer relaties (voor marktaandeel)
- `demografie.parquet` - Schone demografische data met clusters

### 02_coverage.ipynb
**Wat doet het:** Berekent hoe goed Nederland gedekt is door Pon dealers.

**Belangrijkste stappen:**
1. Gebruikt Haversine formule voor afstandsberekening tussen postcodes en dealers
2. Maakt KD-tree voor snelle nearest neighbor search
3. Berekent coverage percentages voor verschillende afstanden (5-15km)
4. Identificeert white spots (gebieden >7.5km van Pon dealer)
5. Analyseert dealer proximity voor kannibalisatie risico

**Output:**
- `coverage_overall.csv` - Coverage percentages per radius
- `white_spots_ranked.csv` - 66 ondervertegenwoordigde gebieden
- `proximity_kpis.csv` - Kannibalisatie vs concurrentie metrics

### 03_kpis_viz.ipynb
**Wat doet het:** Berekent KPIs per gemeente en provincie voor management rapportage.

**Belangrijkste stappen:**
1. Aggregeert dealers naar gemeente en provincie niveau
2. Berekent dealers per 100k inwoners
3. Berekent Pon market share per regio
4. Maakt visualisaties voor board presentatie
5. Identificeert top/bottom performers

**Output:**
- `gemeente_kpis.csv` - KPIs voor 817 gemeenten
- `provincie_kpis.csv` - KPIs voor 7 provincies
- Diverse PNG visualisaties voor presentatie

### 04_enrichment.ipynb
**Wat doet het:** Voegt externe data toe zoals zero-emissie zones.

**Belangrijkste stappen:**
1. Integreert 29 ZE-zone steden met policy index
2. Koppelt policy scores aan white spots
3. Prioriteert gebieden op basis van beleid
4. Analyseert cargo bike potentieel in ZE zones

**Output:**
- `policy_index.csv` - Beleidsscores per gemeente
- `white_spots_with_policy.csv` - White spots met policy weging

### 05_intl_shortlist.ipynb
**Wat doet het:** Analyseert internationale expansie mogelijkheden voor Urban Arrow.

**Belangrijkste stappen:**
1. Verzamelt cycling modal share data voor Europa
2. Analyseert steden vergelijkbaar met Nederlandse UA success stories
3. Berekent opportunity scores op basis van dichtheid, beleid, fiets cultuur


**Output:**
- `ua_intl_shortlist.csv` - Top steden voor UA expansie
- `ua_intl_academic_analysis.csv` - Wetenschappelijke onderbouwing

### 06_portfolio_advies.ipynb
**Wat doet het:** Geeft strategisch advies over het brand portfolio.

**Belangrijkste stappen:**
1. Analyseert brand performance (dealers, ratings, reviews)
2. Meet kannibalisatie tussen Pon merken
3. Berekent incremental coverage per merk
4. Geeft expand/maintain/evaluate advies per merk

**Output:**
- `portfolio_recommendations.csv` - Strategisch advies per merk
- `multi_pon_dealers.csv` - Dealers met meerdere Pon merken

### 07_multi_brand_analysis.ipynb
**Wat doet het:** Analyseert de multi-brand dealer realiteit.

**Belangrijkste stappen:**
1. Identificeert 1,374 multi-brand locaties
2. Categoriseert dealers (Non-Pon, Single Pon, Multi Pon)
3. Berekent brand diversiteit metrics
4. Maakt dashboard-ready dataset

**Output:**
- `dealers_dashboard.parquet` - Enhanced dataset voor Streamlit dashboard

## Dashboard (app/streamlit_app.py)

Interactieve visualisatie van het dealer netwerk met:
- Kaart met alle dealers (blauw=Pon, rood=concurrent)
- Coverage rings visualization
- White spots tabel
- Multi-brand analytics
- Provincial market penetration charts

Start met: `streamlit run app/streamlit_app.py`

## Hoe berekenen we afstanden tussen dealers en postcodes?

Dit project moet voor elk postcodegebied in Nederland weten wat de dichtstbijzijnde Pon dealer is. Met 4,073 postcodes en 2,080 dealers betekent dit miljoenen afstandsberekeningen. Hier is hoe we dat aanpakken:

### De Haversine formule
We gebruiken een wiskundige formule die de kortste afstand over de aardbol berekent tussen twee punten. Dit heet de Haversine formule. Stel je voor dat je een touwtje strak spant over een globe tussen twee punten - dat is de afstand die we berekenen.

**Wat gaat erin:**
- GPS coordinaten van punt A (bijvoorbeeld: 52.3676° N, 4.9041° E voor Amsterdam)
- GPS coordinaten van punt B (bijvoorbeeld: 51.9225° N, 4.4792° E voor Rotterdam)

**Wat komt eruit:**
- De afstand in kilometers tussen deze twee punten (in dit geval ongeveer 57 km)

### Waarom niet gewoon alle afstanden uitrekenen?
Met 4,073 postcodes x 978 Pon dealers = bijna 4 miljoen berekeningen alleen voor Pon dealers. Dat duurt te lang. Daarom gebruiken we een slimme truc.

### De KD-tree oplossing
Een KD-tree is een datastructuur die coordinaten slim organiseert zodat je snel de dichtstbijzijnde punten kunt vinden zonder alles te hoeven uitrekenen. Het is als een telefoonboek voor coordinaten - je hoeft niet het hele boek door te bladeren om iemand te vinden.

**Hoe werkt het:**
1. Alle dealer coordinaten worden in een boom-structuur gezet (duurt 1 seconde)
2. Voor elke postcode vragen we: "wat is de dichtstbijzijnde dealer?"
3. De KD-tree geeft het antwoord in microseconden zonder alle 978 dealers te checken

### Belangrijke beperkingen
**We meten vogelvlucht afstand, niet de werkelijke route:**
- Onze berekening: 7.5 km hemelsbreed
- Werkelijkheid: misschien 9-10 km fietsen via straten
- Een rivier of snelweg tussendoor? Daar houden we geen rekening mee

**Waarom doen we dit zo?**
- Route-berekeningen via Google Maps voor 4,073 postcodes zou dagen duren en veel geld kosten
- Voor strategische beslissingen is vogelvlucht afstand accuraat genoeg
- In Nederland zijn de verschillen meestal klein (geen bergen, goede infrastructuur)

### Wat betekent dit voor de analyse?
- Onze "7.5 km service radius" aannamen is conservatief - mensen fietsen waarschijnlijk verder
- White spots kunnen in werkelijkheid beter bereikbaar zijn dan de data suggereert
- Voor een eerste analyse en strategische beslissingen is deze methode prima
- Voor definitieve locatiekeuzes zou je wel echte route-afstanden willen gebruiken

## Installatie

```bash
pip install -r requirements.txt
```

Benodigde packages:
- pandas, numpy voor data processing
- plotly, matplotlib voor visualisaties
- streamlit voor dashboard
- folium voor interactieve kaarten
- scipy voor afstandsberekeningen

## Runnen van de analyse

Voer notebooks uit in volgorde:
```bash
jupyter notebook notebooks/01_dataprep.ipynb
jupyter notebook notebooks/02_coverage.ipynb
jupyter notebook notebooks/03_kpis_viz.ipynb
jupyter notebook notebooks/04_enrichment.ipynb
jupyter notebook notebooks/05_intl_shortlist.ipynb
jupyter notebook notebooks/06_portfolio_advies.ipynb
jupyter notebook notebooks/07_multi_brand_analysis.ipynb
```

Of automatisch:
```bash
jupyter nbconvert --execute notebooks/*.ipynb --inplace
```

## Belangrijke aannames

- Dealer ontdubbeling op basis van google_place_id
- Afstanden zijn hemelsbreed, niet over de weg
- Standaard service radius: 7.5km (fietsafstand)
- CBS waarde -99997 wordt als missing behandeld
- Multi-brand dealers zijn de norm, niet uitzondering

## Output structuur

```
outputs/
├── tables/          # CSV exports voor analyse
├── figures/         # Visualisaties voor presentatie
└── analysis_reports/ # Gedetailleerde markdown rapporten
```

## Contact

vanvliet.liam@gmail.com