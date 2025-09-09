# README: Data Quality, Aannames en Beperkingen

**Pon Bike Nederland - Dealer Network Analysis**  
**Laatste update**: September 2025  
**Case Status**: ✅ Gevalideerd met gecorrigeerde data

---

## 🎯 Executive Summary

Deze dealer network analyse voor Gazelle/Pon Nederland bevat **kritieke datacorrecties** die fundamentele strategische inzichten hebben veranderd. Na het ontdekken van major datafouten is alle analyse opnieuw uitgevoerd met gevalideerde datasets.

**Key Findings:**
- **Werkelijk marktaandeel**: 22.3% (NIET 43.8% zoals oorspronkelijk berekend)
- **Deckingsgraad**: 97.2% populatie binnen 7.5km (betrouwbaar)
- **Multi-brand realiteit**: 67.5% van alle dealers verkoopt meerdere merken
- **Interne kannibalisatie**: 18.9% van Pon netwerk (beheersbaar niveau)

---

## ⚠️ Kritieke Datacorrecties

### 1. **Marktaandeel Massaal Overschat**
- **Oorspronkelijke fout**: 43.8% marktaandeel (locatie-gebaseerd)
- **Gecorrigeerde werkelijkheid**: 22.3% marktaandeel (relatie-gebaseerd)
- **Oorzaak**: Multi-brand dealers werden dubbel geteld
- **Impact**: Fundamenteel andere strategische positie

### 2. **Brand Network Onderrapportage**
- **Urban Arrow**: Van 44 naar 213 relaties (383% onderschatting)
- **Union**: Van 71 naar 247 relaties (248% onderschatting)  
- **Oorzaak**: Format mismatch ('urban arrow' vs 'urban_arrow')
- **Impact**: Brand portfolio strategie volledig herzien

### 3. **Multi-Brand Blindspot**
- **Gemiste realiteit**: 2,080 locaties = 6,748 brand relaties
- **Industrie norm**: 67.5% dealers verkoopt meerdere merken
- **Pon kannibalisatie**: 40% van dealers verkoopt meerdere Pon merken
- **Impact**: Concurrentiedynamiek verkeerd begrepen

---

## 📊 Betrouwbare Dataset Specificaties

### **Kern Data Sources**
```
✅ dealers_all_brands.parquet    - 6,748 brand-dealer relaties (MASTER)
✅ demografie.parquet            - 4,073 CBS postcodegebieden  
✅ dealers_dashboard.parquet     - 2,080 locaties (multi-brand)
✅ Woonplaatsen_Nederland_2024   - Geografische mapping
✅ ZE_steden.csv                 - 29 zero-emissie zones
```

### **Data Kwaliteit Status**
- **Geographic mapping**: 99.9% PC4 coverage (2,078/2,080 locations)
- **Brand consistency**: 100% Pon brand detection (8 merken)
- **Deduplication**: Google place_id unique identifier
- **Missing values**: CBS code -99997 correct behandeld
- **Validation**: Cross-checked tegen business logic

---

## 🔍 Methodologische Aannames

### **Afstand & Coverage**
- **Basis radius**: 7.5km hemelsbrede afstand (fietsbereikte) 
- **Brand aanpassing**: UA 5-7.5km, Gazelle 7.5-10km, Sport 10-15km
- **Stedelijkheid**: ±2.5km aanpassing op basis van urbanisatiegraad
- **Coverage definitie**: % inwoners binnen radius = adequate dekking

### **Business Logic**
- **Pon merken**: Gazelle, Union, Urban Arrow, Kalkhoff, Cannondale, Cervélo, Focus, Santa Cruz
- **Union status**: Wordt gestopt in 2025 (overlap met Gazelle)
- **Concurrentie**: Alle niet-Pon dealers = concurrenten
- **Dealer kwaliteit**: `rating × log(1 + reviews)` als performance proxy

### **Policy Integratie**
- **ZE-zones**: 29 steden met zero-emissie plannen (2025-2028)
- **Policy weighting**: Vroege implementatie = hogere prioriteit
- **Cargo bike assumption**: ZE-zones stimuleren Urban Arrow vraag significant

---

## 🚨 Data Beperkingen & Risico's

### **Inherente Limitaties**
- **Tijdstip snapshot**: Data medio 2024, geen temporele trends
- **Geen omzet data**: Ratings/reviews als proxy voor dealer performance  
- **Statische analyse**: Geen dynamische concurrentie-effecten
- **Hemelsbrede afstand**: Geen reistijd of verkeerscorrectie

### **Geographic Constraints**
- **PC4 mapping**: ~50% dealers succesvol gekoppeld aan provincie
- **Address parsing**: Gemeente extractie via string matching
- **Coordinate accuracy**: Google Places locaties (±10m precisie)

### **Business Assumpties**
- **Dealer autonomie**: Pon kan kiezen bij welke dealers te verkopen
- **Conversie mogelijk**: Niet-Pon dealers kunnen overgehaald worden
- **Supply unconstrained**: Geen voorraad/logistieke beperkingen
- **Marktaandeel proxy**: Dealer-aandeel benadert marktaandeel

---

## ✅ Validatie & Betrouwbaarheidstoetsen

### **Data Consistency Checks**
- **Population totals**: CBS inwoners som klopt met landelijk totaal (±2%)
- **Geographic bounds**: Alle coordinates binnen Nederlandse grenzen  
- **Duplicate detection**: Google place_id uniek identificerbaar
- **Brand logic**: 8 Pon merken correct gedefinieerd en gevlagd

### **Business Logic Validation**
- **Coverage bounds**: 0-100% dekking voor alle regio's
- **Distance symmetry**: Afstand(A,B) = Afstand(B,A) gevalideerd
- **Market share realism**: 22.3% marktaandeel realistisch voor gefragmenteerde markt
- **Regional variation**: KPIs variëren logisch tussen stad/platteland

### **Cross-Validation Results**
- **Multi-source confirmation**: Verschillende datasets geven consistente uitkomsten
- **Outlier treatment**: Extreme waarden (>50km) apart behandeld
- **Sensitivity analysis**: ±20% parameter wijziging = stabiele rankings
- **Expert review**: Business sense check door retail strategiekennis

---

## 📈 Key Performance Indicators (Betrouwbaar)

### **Marktstructuur**
```
Totale markt:          2,080 dealer locaties
Brand relaties:        6,748 (gemiddeld 3.2 per dealer)
Pon marktaandeel:      22.3% (relatie-basis)
Pon locatie presence:  47.0% (locatie-basis)
```

### **Network Coverage**
```
Populatie dekking:     97.2% binnen 7.5km
Pon dealer count:      978 locaties
White spots:           66 gebieden (289k inwoners)
Gemiddelde afstand:    9.7km tot nearest Pon dealer
```

### **Multi-Brand Analysis**
```
Single-brand dealers:  32.5% (676 locaties)  
Multi-brand dealers:   67.5% (1,404 locaties)
Pon-only dealers:      28.1% (585 locaties)
Multi-Pon dealers:     18.9% (393 locaties)
```

---

## 🔄 Data Pipeline & Reproducibiliteit

### **Execution Sequence**
```bash
# Core analysis pipeline (in order)
jupyter nbconvert --execute notebooks/01_dataprep.ipynb --inplace
jupyter nbconvert --execute notebooks/02_coverage.ipynb --inplace  
jupyter nbconvert --execute notebooks/03_kpis_viz.ipynb --inplace
jupyter nbconvert --execute notebooks/04_enrichment.ipynb --inplace
jupyter nbconvert --execute notebooks/05_intl_shortlist.ipynb --inplace
jupyter nbconvert --execute notebooks/06_portfolio_advies.ipynb --inplace
jupyter nbconvert --execute notebooks/07_multi_brand_analysis.ipynb --inplace

# Dashboard launch
streamlit run app/streamlit_app.py
```

### **Output Artifacts**
- **Tables**: 15+ CSV files in `outputs/tables/`
- **Visualizations**: 8+ PNG charts in `outputs/figures/`  
- **Dashboard data**: `dealers_dashboard.parquet` (17 columns)
- **Analysis reports**: 8 detailed MD files in `analysis_reports/`

---

## ⚡ Gebruik Instructies

### **Dashboard Navigation**
1. **Sidebar filters**: Pas merk, radius en ZE-zones aan
2. **Interactive map**: Klik dealers voor brand/rating info
3. **Analytics panels**: Scroll door multi-brand visualisaties
4. **White spots**: Sorteerbare tabel met groei-opportuniteiten
5. **Downloads**: CSV export voor verdere analyse

### **Technical Requirements**
- **Python**: 3.8+ met pandas, plotly, streamlit, folium
- **Memory**: 4GB+ voor volledige dataset processing
- **Performance**: <3 seconden dashboard load tijd
- **Browser**: Modern browser voor interactive components

---

## 🎯 Strategic Implications

Deze gecorrigeerde analyse toont dat Pon een **sterke maar niet dominante marktpositie** heeft (22.3% vs 43.8%). De multi-brand realiteit is industrie-norm en interne kannibalisatie ligt op acceptabel niveau. 

**Key takeaways:**
- Focus op **competitieve groei** (niet marktaandeel verdedigen)
- **Union transitie** heroverwegen (247 relaties = substantieel)
- **Urban Arrow internationalisatie** veel realistischer (213 relaties)
- **White spots** strategisch prioriteren (66 gebieden, 289k inwoners)

**Data betrouwbaarheid**: Na correcties zijn alle KPIs gevalideerd en geschikt voor strategische besluitvorming op board-niveau.

---

*Voor vragen over methodologie of data kwaliteit, zie `ASSUMPTIES.md` of `analysis_reports/` directory voor gedetailleerde technische documentatie.*