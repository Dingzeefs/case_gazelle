# Kritische Analyse: Voldoet het plan aan de case-eisen?

## 1. DIRECTE CASE VRAGEN - Voldoen we?

### ✅ Vraag 1: "In welke regio's zijn we te veel, goed, of juist weinig aanwezig?"
**Status: VOLDOENDE behandeld, maar kan CONCRETER**

Het plan behandelt dit via:
- Coverage analyse (% inwoners binnen R km)
- Dealers per 100k inwoners
- White spot identificatie
- Proximity/kannibalisatie analyse

**MISSEND:**
- Geen expliciete definitie van "te veel" (bijv. >3 dealers/100k = overbediend)
- Geen benchmark met landelijk gemiddelde per regio-type
- Geen concrete output: "Top 10 overbediende gemeenten" lijst

**VERBETERING NODIG:**
```python
# Definieer thresholds:
overbediend = dealers_per_100k > nl_avg * 1.3
goed_bediend = (nl_avg * 0.7) <= dealers_per_100k <= (nl_avg * 1.3)  
onderbediend = dealers_per_100k < nl_avg * 0.7
```

### ⚠️ Vraag 2: "Urban Arrow internationale expansie advies"
**Status: ALGEMEEN behandeld, maar MIST CONCRETE LANDEN**

Het plan noemt:
- Denemarken, Duitsland, België als mogelijkheden
- Criteria: fietscultuur, urbanisatie, ZE-beleid
- B2B + B2C strategie

**KRITISCH MISSEND:**
- Geen data-analyse van specifieke landen
- Geen vergelijking met NL-benchmark cijfers
- Geen concrete stad-selectie met cijfers
- Geen dealer-dichtheid targets voor nieuwe markt

**VERBETERING:**
- Voeg tabel toe: "Top 5 steden voor UA expansie" met scores
- Bereken: hoeveel dealers nodig per stad voor 80% coverage
- Timeline: Q1-Q4 rollout plan per stad

### ❌ Vraag 3: "Portfolio advies (stoppen/toevoegen) met CSR/politiek"
**Status: TE ABSTRACT, mist data-onderbouwing**

Het plan noemt:
- Union gestopt, GT on hold
- Adaptive mobility kans
- CSR via ZE-zones

**GROTE GATEN:**
- Geen analyse van merkprestaties in de data
- Geen kannibalisatie-matrix tussen merken
- Geen concrete CSR-score per merk
- Geen politieke analyse (bijv. subsidies, regelgeving)

**KRITISCHE TOEVOEGING NODIG:**
```python
# Merk performance analyse:
- Revenue proxy: dealers * avg_rating * reviews
- Overlap analyse: % dealers met >1 Pon merk
- Growth potential: white spots geschikt voor merk X
- CSR score: % dealers in ZE-zones, urban coverage
```

## 2. DELIVERABLES CHECK

### ✅ Slide deck (max 15 min)
Plan heeft 10 slides outline - OK maar mist:
- Concrete getallen per slide
- Visualisatie voorbeelden
- Executive summary met 3 key numbers

### ⚠️ Werkend notebook/script
Notebooks genoemd maar NIET geïmplementeerd:
- `01_dataprep.ipynb` - leeg
- `02_coverage.ipynb` - bevat alleen {}
- `03_kpis_viz.ipynb` - leeg

### ❌ Dashboard (Tableau/Power BI/Excel)
Alleen Streamlit app genoemd, maar:
- Geen filters voor ALLE merken
- Geen scenario vergelijking
- Geen export functie voor board

### ⚠️ README met aannames
README bestaat maar mist:
- Datakwaliteit issues (hoeveel NULL values?)
- Validatie resultaten
- Gevoeligheidsanalyse parameters

## 3. KPI'S VOLLEDIGHEID

### Gevraagde KPI's vs Plan:
✅ Dealers per 100k - aanwezig
✅ Pon-share - aanwezig  
⚠️ Coverage vs UA benchmark - genoemd maar niet uitgewerkt
✅ White spots - uitgebreid behandeld
⚠️ Concurrentie-intensiteit - basis aanwezig, mist diepgang

### MISSENDE KPI's:
- **Merk-specifieke performance** per regio
- **Groei-potentieel score** per gemeente
- **ROI projectie** voor voorgestelde changes
- **Kannibalisatie risico score**

## 4. DATA GEBRUIK - Kritische issues

### Demografie data ONDERBENUT:
De case geeft specifiek aan: "inkomens, huishoudens, leeftijden, gezinnen"

**NIET GEBRUIKT:**
- Inkomen → koopkracht voor premium merken
- Gezinssamenstelling → Urban Arrow Family potentieel
- Leeftijd → e-bike vs traditioneel
- Huishoudgrootte → cargo bike need

**MOET TOEVOEGEN:**
```python
# Demografie scoring:
ua_potential = (
    0.3 * z(gezinnen_met_kinderen) +
    0.3 * z(inkomen_hoog) +
    0.2 * z(25_44_jaar) +
    0.2 * z(stedelijkheid)
)
```

### PC4 gemeente mapping PROBLEEM:
File `pc4_gemeente.csv` is LEEG voor gemeente kolom!
Dit breekt de hele regio-analyse.

**URGENT FIX:**
- Gebruik pgeocode library voor PC4→gemeente
- Of gebruik eerste 2 cijfers PC4 voor provincie

## 5. EIGEN INBRENG - Wat ontbreekt?

### Creativiteit/Innovatie GEMIST:
1. **Geen predictive model** voor dealer success
2. **Geen customer journey** analyse
3. **Geen seasonality** in planning
4. **Geen competitive response** scenario's
5. **Geen social media/review** sentiment analyse

### Business sense ZWAK:
- Geen business case met euro's
- Geen risico matrix
- Geen implementation roadmap met owners
- Geen success metrics/KPI targets

## 6. CONCRETE VERBETERACTIES

### MUST HAVE voor case:
1. **Implementeer notebooks** met werkende code
2. **Bereken concrete getallen** voor elke slide
3. **Maak merk-analyse** met kannibalisatie matrix
4. **Voeg CSR scorecard** toe met gewichten
5. **Bouw interactief dashboard** met alle filters

### Data fixes:
```python
# 1. Fix PC4 mapping
import pgeocode
nomi = pgeocode.Nominatim('nl')
df['gemeente'] = df['pc4'].apply(lambda x: nomi.query_postal_code(str(x).zfill(4)).county_name)

# 2. Clean demografie
df.replace(-99997, np.nan, inplace=True)
df['inkomen_schoon'] = df['inkomen'].fillna(df.groupby('gemeente')['inkomen'].transform('median'))

# 3. Merk performance
merk_kpi = df.groupby('brand_clean').agg({
    'google_place_id': 'nunique',  # aantal dealers
    'google_rating': 'mean',
    'google_user_ratings_total': 'sum',
    'is_pon': 'mean'  # % van merk dat Pon is
})
```

### Visualisatie upgrades:
1. **Kannibalisatie heatmap**: correlation matrix tussen merken
2. **Portfolio bubble chart**: x=groei, y=share, size=revenue
3. **Scenario slider**: wat als +10 dealers impact
4. **Gemeente ranking**: sorteerbare tabel alle KPIs

## 7. EINDOORDEEL

**Score: 6/10** - Basis aanwezig maar niet case-ready

### Sterke punten:
+ Goede structuur en methodiek
+ Proximity analyse innovatief
+ ZE-beleid integratie relevant

### Kritieke missers:
- Geen werkende code/notebooks
- Demografie data niet gebruikt
- Portfolio advies te abstract
- Concrete getallen ontbreken
- Business case/ROI missend

### URGENT voor presentatie:
1. Maak minimaal 3 werkende notebooks
2. Bereken ALLE KPI's met echte getallen
3. Bouw simpel dashboard (zelfs Excel is OK)
4. Maak 5 concrete aanbevelingen met cijfers
5. Voeg portfolio-analyse met data toe

**Bottom line:** Het plan is academisch sterk maar mist de praktische uitvoering en concrete cijfers die de board verwacht. Focus op UITVOEREN, niet plannen!