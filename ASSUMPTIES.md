# Assumpties en Beperkingen - Gazelle/Pon Bike Case

## Data Assumpties

### Dealer Data (`dealer_lijst.csv`)
- **Unieke dealer identificatie**: `google_place_id` is betrouwbaar en consistent
- **Meerdere merken per dealer**: E�n dealer kan meerdere regels hebben (��n per merk)
- **Data volledigheid**: Alle significante fietsendealers in Nederland zijn opgenomen
- **Locatie accuraatheid**: Google Places lat/lng zijn accuraat genoeg voor afstandsberekeningen
- **Rating representativiteit**: Google ratings weerspiegelen dealer kwaliteit/populariteit
- **Tijdstip snapshot**: Data representeert situatie medio 2024, geen seizoensvariatie

### Demografie Data (`demografie.csv`)
- **CBS code -99997**: Betekent "0-4 waarde / geheim / niet aanwezig" 
  - Voor tellingen (inwoners): vervangen door 0
  - Voor percentages/ratio's: vervangen door NaN
- **PC4 representativiteit**: Alle Nederlandse postcodegebieden zijn vertegenwoordigd
- **Tijdstip**: CBS data is recentste beschikbare (2023-2024)
- **Aggregatie validiteit**: Optellen van PC4 naar gemeente/provincie geeft correcte totalen

### Geografische Mapping
- **Woonplaatsen data**: `Woonplaatsen_in_Nederland_2024_*.csv` is compleet en actueel
- **Plaats�Gemeente mapping**: Dealers kunnen betrouwbaar gekoppeld worden via plaatsnaam
- **PC4�Gemeente**: Originele `pc4_gemeente.csv` is incompleet - woonplaatsen data wordt gebruikt
- **Geografische hi�rarchie**: Plaats � Gemeente � Provincie � Landsdeel is consistent

## Business Assumpties

### Markt & Concurrentie
- **Pon merken definitie**: Gazelle, Cannondale, Union, Kalkhoff, Urban Arrow, Cerv�lo, Focus, Santa Cruz
- **Union status**: Merk wordt gestopt per 2025 (overlap met Gazelle)
- **GT Bicycles**: On hold/geliquideerd (overlap met andere Pon sportmerken)
- **Concurrentie definitie**: Alle niet-Pon fietsendealers zijn concurrenten
- **Marktaandeel proxy**: Dealer-aandeel benadert marktaandeel redelijk

### Urban Arrow Benchmark
- **Succesvol netwerk**: UA's huidige Nederlandse netwerk wordt als "succesvol" beschouwd
- **Target dekking**: UA haalt doelen met huidige dealer setup
- **Benchmark geldigheid**: UA's strategie is toepasbaar op andere Pon merken
- **Premium positionering**: UA's selectieve dealer-aanpak is juiste strategische richting

### Dealer Strategie�n
- **Dealer autonomie**: Pon heeft vrijheid om te kiezen bij welke dealers ze verkopen
- **Dealer kwaliteit**: `rating � log(1 + reviews)` is redelijke proxy voor dealer performance
- **Service capaciteit**: Dealers kunnen meerdere Pon merken adequaat bedienen
- **Conversie mogelijkheid**: Niet-Pon dealers kunnen overgehaald worden om Pon te verkopen

## Methodologische Assumpties

### Afstand & Coverage
- **Afstandsmeting**: Haversine (hemelsbrede) afstand is acceptabele benadering
- **Geen reistijd**: Verkeerssituatie en infrastructuur worden genegeerd
- **Uniforme radius**: 7.5 km basis-radius voor alle locaties (met stedelijkheidsaanpassing)
- **Coverage definitie**: % inwoners binnen radius = adequate dekking
- **Brand-specifieke radius**:
  - Urban Arrow: 5-7.5 km (premium cargo, kortere afstand)
  - Gazelle: 7.5-10 km (mainstream e-bikes)
  - Sport merken (Cannondale/Cerv�lo): 10-15 km (specialty, langere afstand)

### Stedelijkheidsaanpassingen
- **Zeer stedelijk**: -2.5 km van basis radius (meer dealers/concurrentie)
- **Sterk stedelijk**: Basis radius (7.5 km)
- **Matig stedelijk**: +2.5 km van basis radius
- **Weinig/niet stedelijk**: +5 km van basis radius (minder dealers)

### Demografie Weging
- **Gezinnen belangrijk**: Huishoudens met kinderen hebben hogere fiets-behoefte
- **Inkomen correlatie**: Hogere inkomens kopen duurdere/premium fietsen
- **Leeftijd relevantie**: 25-44 jaar is primaire doelgroep voor (cargo)bikes
- **Urbanisatie factor**: Stedelijke gebieden hebben hogere fiets-behoefte

### KPI Berekeningen
- **Dealers per 100k**: Standard density metric voor retail netwerk analyse
- **Pon-share**: % Pon dealers van totaal dealers per regio
- **Coverage benchmark**: UA's huidige coverage als target voor andere merken
- **White spot prioritering**: Hoge bevolking + lage concurrentie = beste kansen

## Policy & Externe Factoren

### Zero-Emissie Zones
- **Beleid impact**: ZE/LEZ zones drijven significant cargo bike vraag
- **Policy index**: Vroege implementatie (2025) = hogere score dan late (2027+)
- **Geographic scope**: ZE-zones beperken zich tot stadscentra, niet hele gemeenten
- **Cargo bike substitutie**: Elektrische bakfietsen vervangen bestelwagens in ZE-zones

### CSR & Politiek
- **Duurzaamheidsweging**: E-bikes en cargo bikes krijgen hogere prioriteit
- **Politieke steun**: Gemeenten ondersteunen fiets-mobiliteitsprojecten
- **Subsidie aannames**: Geen directe subsidies meegenomen in business case
- **Regelgeving stabiliteit**: Huidige ZE-plannen worden uitgevoerd zoals gepland

## Internationale Expansie

### Vergelijkbare Landen
- **Cultural similarity**: Denemarken, Duitsland, Belgi� hebben vergelijkbare fietscultuur
- **Policy alignment**: Landen met ZE-plannen zijn geschikt voor UA expansie  
- **Economic conditions**: GDP/capita >�30k ondersteunt premium fiets-aanschaf
- **Urban density**: >2000 adressen/km� nodig voor viable cargo bike market

### Expansie Strategie
- **Premium first**: Start met hoogwaardige dealers in beste locaties
- **B2B focus**: Zakelijke markt (last-mile delivery) sneller dan particulier
- **Minimum spacing**: 3-5 km tussen UA dealers om kannibalisatie te voorkomen
- **Gradual rollout**: Begin in 1-2 steden per land, daarna uitbreiden

## Technische Beperkingen

### Data Kwaliteit
- **Missing values**: -99997 waarden correct ge�nterpreteerd en behandeld
- **Geocoding accuracy**: Google Places locaties accuraat genoeg voor analyse
- **Temporal consistency**: Alle datasets representeren vergelijkbare tijdsperiode
- **Sample bias**: Geen significante systematische onder-/oververtegenwoordiging

### Model Limitaties
- **No revenue data**: Gebruik ratings/reviews als proxy voor dealer performance
- **Static analysis**: Geen dynamische effecten (seizoen, trends, concurrentie-reactie)
- **No supply constraints**: Aangenomen dat Pon alle dealers kan bevoorraden
- **Simplified competition**: Concurrenten reageren niet op Pon's moves

### Computational Assumpties
- **Haversine accuracy**: <1% fout voor Nederland is acceptabel
- **Z-score normalisatie**: Features zijn redelijk normaal verdeeld
- **Linear relationships**: Scoring weights zijn lineair combineerbaar
- **Threshold stability**: Gevoeligheidsanalyse toont robuuste resultaten binnen �20%

## Validatie & Sanity Checks

### Data Validatie
- **Population totals**: Som van PC4 inwoners = CBS landelijk totaal (binnen 5%)
- **Geographic consistency**: Dealer coordinates liggen binnen Nederlandse grenzen
- **Duplicate detection**: Google place_id duplicates correct ge�dentificeerd
- **Outlier treatment**: Extreme waarden (>50km nearest neighbor) apart behandeld

### Business Logic Checks
- **Coverage bounds**: 0% d coverage d 100% voor alle regio's
- **Dealer counts**: Aantal unieke dealers klopt met werkelijkheid
- **Brand consistency**: Pon brand flagging correct voor alle 8 merken
- **Distance symmetry**: Afstand(A,B) = Afstand(B,A) voor alle dealer pairs

### Results Plausibility
- **Regional variation**: KPIs vari�ren logisch tussen stad/platteland
- **Brand performance**: Premium merken hebben lagere densiteit, hogere coverage
- **White spot rankings**: Top white spots zijn herkenbare ondervertegenwoordigde gebieden
- **International targets**: Voorgestelde steden hebben logische similarity met NL

## Risico's & Mitigaties

### Data Risico's
- **Incomplete dealer list**: Gemiste dealers � onderschatting concurrentie (laag risico)
- **Outdated information**: Gesloten/nieuwe dealers niet bijgewerkt (medium risico)
- **Geographic misalignment**: Verkeerde plaats-gemeente koppeling (laag risico door validatie)

### Model Risico's
- **Parameter sensitivity**: Scoring weights be�nvloeden rankings (mitigatie: gevoeligheidsanalyse)
- **Linear assumptions**: Werkelijkheid is complexer dan lineaire modellen (medium risico)
- **Static projections**: Markt verandert sneller dan model (hoog risico voor lange termijn)

### Business Risico's
- **Competitive response**: Concurrenten reageren op Pon's expansie (hoog risico)
- **Regulatory changes**: ZE-beleid verandert sneller dan verwacht (medium risico)
- **Economic downturn**: Fiets-markt conjunctuurgevoelig (medium risico)
- **Technology disruption**: Nieuwe mobiliteitsvormen (e-scooters, MaaS) (medium risico)

## Implementatie Assumpties

### Tijdlijn & Resources
- **Development time**: 2 dagen voor volledige case implementatie
- **Data processing**: Notebooks runnen binnen 30 minuten op standaard laptop
- **Dashboard performance**: <3 seconden load time met volledige dataset
- **Presentation prep**: 4 uur voor slide deck en Q&A voorbereiding

### Skill Assumpties
- **Python proficiency**: Pandas, GeoPandas, Plotly, Streamlit gebruik
- **Domain knowledge**: Basis retail/netwerk strategie concepten
- **Presentation skills**: Board-level communicatie in 15 minuten
- **Business acumen**: Vertaling van data naar strategische adviezen

### Success Criteria
- **Technical**: Alle code werkt reproduceerbaar zonder errors
- **Analytical**: Alle 3 case-vragen beantwoord met concrete data
- **Strategic**: Actionable recommendations met business case
- **Communication**: Heldere visualisaties en executive summary

---

## ACTUELE ANALYSE RESULTATEN (September 2025) - KRITISCHE CORRECTIES

### ⚠️ KRITISCHE DATA KWALITEITSFOUTEN ONTDEKT & GECORRIGEERD

#### **1. MARKTAANDEEL MASSAAL OVERSCHAT**
- **FOUT**: Aangenomen 43.8% marktaandeel (locatie-gebaseerd)
- **WERKELIJKHEID**: 22.3% marktaandeel (relatie-gebaseerd) - BIJNA 50% LAGER
- **OORZAAK**: Multi-brand dealers werden dubbel geteld voor Pon
- **IMPACT**: Strategische arrogantie, onderschatting concurrentie, verkeerde prioriteiten

#### **2. BRAND NETWERK DATA COMPLEET FOUT**
- **Urban Arrow FOUT**: Gerapporteerd 44 dealers → WERKELIJK 213 relaties (383% onderrapportage!)
- **Union FOUT**: Gerapporteerd 71 dealers → WERKELIJK 247 relaties (248% onderrapportage!)
- **Gazelle FOUT**: Gerapporteerd 584 dealers → WERKELIJK 701 relaties (20% onderrapportage)
- **OORZAAK**: PON_BRANDS definitie gebruikte 'urban arrow' (spatie) terwijl data 'urban_arrow' (underscore) heeft

#### **3. MULTI-BRAND REALITEIT GEMIST**
- **GEMISTE INZICHT**: 66.1% van ALLE dealers verkoopt meerdere merken
- **PON CANNIBALISATIE**: 40.0% van Pon dealers verkoopt meerdere Pon merken
- **IMPACT**: Cannibalitatie-risico volledig onderschat, concurrentie-dynamiek verkeerd begrepen

### 📊 GECORRIGEERDE MARKTPOSITIE (WERKELIJKE DATA)

#### **Werkelijke Marktstructuur**:
- **Totale markt**: 2,080 dealer locaties → 6,748 brand-dealer relaties
- **Pon marktaandeel**: **22.3% relaties** (NIET 43.8% locaties) - **REALISTISCHE POSITIE**
- **Multi-brand norm**: 66.1% dealers = industrie standard, NIET Pon probleem
- **Populatie coverage**: 97.2% blijft correct - ENIGE BETROUWBARE METRIC

#### **Gecorrigeerde Brand Performance**:
```
WERKELIJKE NETWERK (relaties):
1. Gazelle: 701 relaties (700 locaties) - 46.5% van Pon netwerk
2. Union: 247 relaties (247 locaties) - 16.4% van Pon netwerk  
3. Urban Arrow: 213 relaties (211 locaties) - 14.1% van Pon netwerk
4. Kalkhoff: 199 relaties (191 locaties) - 13.2% van Pon netwerk
5. Cannondale: 92 relaties (92 locaties) - 6.1% van Pon netwerk
```

#### **Kannibalisatie WERKELIJKHEID**:
- **Multi-Pon locaties**: 391 van 978 Pon dealers (40.0% interne concurrentie)
- **Top kannibalistische paren**: 
  - Gazelle + Union: 186 gezamenlijke locaties
  - Gazelle + Urban Arrow: 114 gezamenlijke locaties
  - Gazelle + Kalkhoff: 108 gezamenlijke locaties

### 🎯 STRATEGISCHE IMPLICATIES VAN CORRECTIES

#### **Van Overmoed naar Realisme**:
- **OUDE ASSUMPTIE**: "Dominante marktleider (43.8%)" → **REALITEIT**: "Sterke #1 speler (22.3%)"
- **OUDE STRATEGIE**: Marktaandeel verdedigen → **NIEUWE STRATEGIE**: Competitief groeien
- **OUDE FOCUS**: White spots vullen → **NIEUWE FOCUS**: Bestaande netwerk optimaliseren

#### **Brand Portfolio Heroverwegen**:
- **Union**: Van "klein merk (71 dealers)" naar "significante speler (247 relaties)" - Exit timing heroverweeg
- **Urban Arrow**: Van "niche premium (44)" naar "substantieel netwerk (213)" - Internationale expansie veel realistischer
- **Focus**: Slechts 8 relaties - DAADWERKELIJKE exit kandidaat

#### **Concurrentie Realiteit**:
- **Multi-brand = norm**: 66.1% is industrie standaard, NIET Pon falen
- **Interne concurrentie acceptabel**: 40.0% Pon kannibalisatie is beheersbaar niveau
- **Externe druk hoger**: 77.7% markt is NON-Pon → competitieve markt

### 🚨 KRITIEKE LESSEN VOOR DATA-DRIVEN BESLUITVORMING

#### **1. NOOIT AANNEMEN, ALTIJD VALIDEREN**
- Single data source leidde tot 50% marktaandeel fout
- Brand naam format mismatch (spatie vs underscore) veroorzaakte 383% fout
- Multi-brand structuur volledig over het hoofd gezien

#### **2. BUSINESS LOGIC VOOR ALLES**
- 43.8% marktaandeel in gefragmenteerde retail? **ONMOGELIJK**
- Urban Arrow 44 dealers voor premium cargo brand? **ONDERMAATS**
- Geen multi-brand dealers in Nederland? **WERELDVREEMD**

#### **3. MEERDERE DATABRONNEN KRUISVALIDEREN**
- Locatie-based vs relatie-based metrics gaven 50% verschil
- Geographic mapping via meerdere methoden valideren
- Business sense checks op ALLE uitkomsten

### 📊 BETROUWBARE FINAL METRICS (Gevalideerd)

#### **Marktstructuur (September 2025)**:
- **Totale retail netwerk**: 2,080 locaties, 6,748 brand-relaties (3.2 merken/dealer gemiddeld)
- **Pon marktpositie**: 22.3% relatie-aandeel, 47.0% locatie-presence
- **Coverage excellence**: 97.2% populatie binnen 7.5km (BEVESTIGD)
- **Viable white spots**: 66 gebieden (289k inwoners) voor strategische groei

#### **Brand Hiërarchie (Betrouwbaar)**:
1. **Gazelle**: Marktleider (701 relaties, 9.0/10 strategische waarde) → EXPAND
2. **Union**: Sterke #2 (247 relaties, 6.2/10 strategische waarde) → MAINTAIN
3. **Urban Arrow**: Premium leader (213 relaties, 7.1/10 CSR) → INTERNATIONAL READY
4. **Kalkhoff**: Sustainability champion (199 relaties, 7.7/10 CSR) → MAINTAIN
5. **Focus**: Exit kandidaat (8 relaties, 5.1/10 strategische waarde) → EVALUATE

#### **Internationale Expansie (Urban Arrow)**:
- **Nederlandse benchmark**: 213 relaties across 148 steden = 1.44 relaties/stad
- **Top targets**: Germany (9.3% mode share), Finland (7.8% mode share)
- **Academic backing**: Goel et al. (2022) cycling research validates targets

### ⚠️ RISICO WAARSCHUWINGEN

#### **Data Dependency Risico's**:
- **Single source danger**: Één dataset leidde tot 50% strategische fout
- **Format assumptions**: Kleine verschillen (spatie vs underscore) = grote impact
- **Business logic gaps**: Technische correctheid ≠ business realiteit

#### **Strategic Decision Risico's**:
- **Overmoed gevaar**: 43.8% vs 22.3% marktaandeel = compleet andere strategie
- **Brand undervaluation**: Urban Arrow bijna 5x groter dan gerapporteerd
- **Competition blindspot**: Multi-brand norm gemist = verkeerde concurrentie-inschatting

---

*KRITISCHE UPDATE: 7 September 2025 - Alle assumpties heroverwogen na ontdekking van fundamentele datafouten. Resultaten nu gebaseerd op gevalideerde, gekruiscontroleerde datasets met business logic verificatie.*