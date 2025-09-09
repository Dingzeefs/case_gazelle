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